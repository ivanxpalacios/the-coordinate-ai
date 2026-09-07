export interface ChatSource {
  chunk_id: string
  source_title: string
  source_url: string
  entity: string | null
  global_number: number
}

export type ChatEvent =
  | { type: 'sources'; sources: ChatSource[] }
  | { type: 'token'; content: string }
  | { type: 'done' }
  | { type: 'error'; message: string }
