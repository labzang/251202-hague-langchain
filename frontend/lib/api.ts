import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp?: Date
  sources?: DocumentSource[]
}

export interface DocumentSource {
  content: string
  metadata?: Record<string, any>
}

export interface RAGResponse {
  question: string
  answer: string
  retrieved_documents: Array<{
    content: string
    metadata?: Record<string, any>
  }>
  retrieved_count: number
}

export const chatAPI = {
  async sendMessage(question: string, k: number = 3): Promise<RAGResponse> {
    const response = await api.post<RAGResponse>('/rag', {
      question,
      k,
    })
    return response.data
  },

  async healthCheck(): Promise<{ status: string }> {
    const response = await api.get('/health')
    return response.data
  },
}

