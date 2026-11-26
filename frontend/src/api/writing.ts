import api from './client'

export interface RewriteRequest {
  text: string
  intensity?: number
  profile?: 'swift' | 'studio' | 'careful' | 'plain'
  language?: string
}

export interface RewriteResponse {
  original: string
  rewritten: string
  word_count: number
  character_count: number
}

export interface DetectRequest {
  text: string
  mode?: 'quick' | 'deep'
}

export interface DetectResponse {
  overall_score: number
  label: string
  highlights: Array<{ text: string; score: number }>
}

export interface SaveDocumentRequest {
  title: string
  content: string
  tool: string
}

export interface Document {
  id: number
  title: string
  content: string
  tool: string
  created_at: string
}

export const writingApi = {
  rewrite: (data: RewriteRequest) => api.post<RewriteResponse>('/writing/rewrite', data),
  paraphrase: (data: RewriteRequest) => api.post<RewriteResponse>('/writing/paraphrase', data),
  essayRewrite: (data: RewriteRequest) => api.post<RewriteResponse>('/writing/essay-rewrite', data),
  articleRewrite: (data: RewriteRequest) => api.post<RewriteResponse>('/writing/article-rewrite', data),
  sentenceRewrite: (data: RewriteRequest) => api.post<RewriteResponse>('/writing/sentence-rewrite', data),
  paragraphRewrite: (data: RewriteRequest) => api.post<RewriteResponse>('/writing/paragraph-rewrite', data),
  contentImprove: (data: RewriteRequest) => api.post<RewriteResponse>('/writing/content-improve', data),
  grammarCheck: (data: RewriteRequest) => api.post<RewriteResponse>('/writing/grammar', data),
  detect: (data: DetectRequest) => api.post<DetectResponse>('/writing/detect', data),
  downloadDocx: (data: RewriteRequest) => api.post('/writing/download-docx', data, { responseType: 'blob' }),
}
