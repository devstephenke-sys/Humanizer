import json

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Document, User
from app.schemas import DocumentCreate, DocumentPublic, DocumentUpdate
from app.services.text_utils import title_from_text


def to_public(document: Document) -> DocumentPublic:
    return DocumentPublic(
        id=document.id,
        title=document.title,
        tool=document.tool,  # type: ignore[arg-type]
        input_text=document.input_text,
        output_text=document.output_text,
        settings_json=document.settings_json,
        created_at=document.created_at,
        updated_at=document.updated_at,
    )


class DocumentService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_for(self, user: User) -> list[DocumentPublic]:
        rows = (
            await self.session.scalars(
                select(Document).where(Document.user_id == user.id).order_by(Document.updated_at.desc())
            )
        ).all()
        return [to_public(row) for row in rows]

    async def get_for(self, user: User, document_id: str) -> Document:
        document = await self.session.scalar(
            select(Document).where(Document.id == document_id, Document.user_id == user.id)
        )
        if document is None:
            raise HTTPException(status_code=404, detail="Document not found.")
        return document

    async def create(self, user: User, payload: DocumentCreate) -> DocumentPublic:
        if len(payload.input_text) > 60_000 or len(payload.output_text) > 60_000:
            raise HTTPException(status_code=413, detail="Document is too large to store.")
        try:
            json.loads(payload.settings_json or "{}")
        except json.JSONDecodeError as exc:
            raise HTTPException(status_code=422, detail="Settings must be JSON.") from exc
        document = Document(
            user_id=user.id,
            title=(payload.title or title_from_text(payload.input_text)).strip() or "Untitled draft",
            tool=payload.tool,
            input_text=payload.input_text,
            output_text=payload.output_text,
            settings_json=payload.settings_json or "{}",
        )
        self.session.add(document)
        await self.session.commit()
        await self.session.refresh(document)
        return to_public(document)

    async def update(self, user: User, document_id: str, payload: DocumentUpdate) -> DocumentPublic:
        document = await self.get_for(user, document_id)
        if payload.title is not None:
            document.title = payload.title.strip() or document.title
        if payload.input_text is not None:
            document.input_text = payload.input_text
        if payload.output_text is not None:
            document.output_text = payload.output_text
        if payload.settings_json is not None:
            try:
                json.loads(payload.settings_json or "{}")
            except json.JSONDecodeError as exc:
                raise HTTPException(status_code=422, detail="Settings must be JSON.") from exc
            document.settings_json = payload.settings_json
        await self.session.commit()
        await self.session.refresh(document)
        return to_public(document)

    async def delete(self, user: User, document_id: str) -> None:
        document = await self.get_for(user, document_id)
        await self.session.delete(document)
        await self.session.commit()
