import api from './client'
import type { Document, SaveDocumentRequest } from './writing'

export const documentsApi = {
  list: () => api.get<Document[]>('/documents'),
  save: (data: SaveDocumentRequest) => api.post<Document>('/documents', data),
  get: (id: number) => api.get<Document>(`/documents/${id}`),
  delete: (id: number) => api.delete(`/documents/${id}`),
}
