from io import BytesIO

from docx import Document as DocxDocument
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database import get_session
from app.models import User
from app.rate_limit import enforce_write_limit
from app.schemas import (
    AlternativesRequest,
    AlternativesResponse,
    AuthResponse,
    DetectRequest,
    DetectResponse,
    DocumentCreate,
    DocumentPublic,
    DocumentUpdate,
    ExportRequest,
    HealthResponse,
    LoginRequest,
    RegisterRequest,
    RewriteRequest,
    RewriteResponse,
    UserPublic,
)
from app.security import create_token, get_current_user, hash_password, verify_password
from app.services.detection import DetectionService
from app.services.documents import DocumentService
from app.services.writing import SERVICE_BY_TOOL, RewriteEngine

router = APIRouter(prefix="/api")
detector = DetectionService()


def user_public(user: User) -> UserPublic:
    return UserPublic(id=user.id, email=user.email, display_name=user.display_name)


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="ok",
        provider=settings.ai_provider,
        provider_configured=settings.provider_configured,
    )


@router.post("/auth/register", response_model=AuthResponse)
async def register(payload: RegisterRequest, request: Request, session: AsyncSession = Depends(get_session)) -> AuthResponse:
    enforce_write_limit(request, "auth")
    existing = await session.scalar(select(User).where(User.email == payload.email.lower()))
    if existing is not None:
        raise HTTPException(status_code=409, detail="An account with that email already exists.")
    user = User(
        email=payload.email.lower(),
        display_name=payload.display_name.strip(),
        password_hash=hash_password(payload.password),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return AuthResponse(token=create_token(user.id), user=user_public(user))


@router.post("/auth/login", response_model=AuthResponse)
async def login(payload: LoginRequest, request: Request, session: AsyncSession = Depends(get_session)) -> AuthResponse:
    enforce_write_limit(request, "auth")
    user = await session.scalar(select(User).where(User.email == payload.email.lower()))
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Email or password is incorrect.")
    return AuthResponse(token=create_token(user.id), user=user_public(user))


@router.get("/auth/me", response_model=UserPublic)
async def me(user: User = Depends(get_current_user)) -> UserPublic:
    return user_public(user)


@router.post("/write", response_model=RewriteResponse)
async def write(payload: RewriteRequest, request: Request) -> RewriteResponse:
    enforce_write_limit(request, "write")
    service_cls = SERVICE_BY_TOOL[payload.tool]
    service = service_cls()
    if isinstance(service, RewriteEngine) and not hasattr(service, "run"):
        return await service.rewrite(payload, payload.tool)
    if payload.tool in {"humanize", "rewrite", "paraphrase", "grammar"}:
        return await service.run(payload)  # type: ignore[attr-defined]
    return await service.rewrite(payload, payload.tool)


@router.post("/write/alternatives", response_model=AlternativesResponse)
async def alternatives(payload: AlternativesRequest, request: Request) -> AlternativesResponse:
    enforce_write_limit(request, "write")
    return await RewriteEngine().alternatives(payload)


@router.post("/detect", response_model=DetectResponse)
async def detect(payload: DetectRequest, request: Request) -> DetectResponse:
    enforce_write_limit(request, "detect")
    settings = get_settings()
    if len(payload.text) > settings.max_input_chars:
        raise HTTPException(status_code=413, detail="Text is too long to scan.")
    return detector.analyze(payload.text, payload.mode)


@router.get("/documents", response_model=list[DocumentPublic])
async def list_documents(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> list[DocumentPublic]:
    return await DocumentService(session).list_for(user)


@router.post("/documents", response_model=DocumentPublic)
async def create_document(
    payload: DocumentCreate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> DocumentPublic:
    return await DocumentService(session).create(user, payload)


@router.get("/documents/{document_id}", response_model=DocumentPublic)
async def get_document(
    document_id: str,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> DocumentPublic:
    document = await DocumentService(session).get_for(user, document_id)
    from app.services.documents import to_public

    return to_public(document)


@router.patch("/documents/{document_id}", response_model=DocumentPublic)
async def update_document(
    document_id: str,
    payload: DocumentUpdate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> DocumentPublic:
    return await DocumentService(session).update(user, document_id, payload)


@router.delete("/documents/{document_id}", status_code=204)
async def delete_document(
    document_id: str,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    await DocumentService(session).delete(user, document_id)


@router.post("/export/docx")
async def export_docx(payload: ExportRequest, request: Request) -> StreamingResponse:
    enforce_write_limit(request, "export")
    if len(payload.text) > get_settings().max_input_chars:
        raise HTTPException(status_code=413, detail="Text is too long to export.")
    document = DocxDocument()
    document.add_heading(payload.title[:180] or "Draft", level=1)
    for block in payload.text.split("\n"):
        document.add_paragraph(block)
    buffer = BytesIO()
    document.save(buffer)
    buffer.seek(0)
    filename = "draftwell.docx"
    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
