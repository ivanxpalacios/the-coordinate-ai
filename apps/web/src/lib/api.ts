import { supabase } from './supabase'
import type { ChatEvent } from '../types/chat'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

export async function registerUser(
  email: string,
  password: string,
  accessCode: string,
): Promise<{ error: string | null }> {
  const response = await fetch(`${API_BASE_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, access_code: accessCode }),
  })

  if (response.ok) return { error: null }

  const body = (await response.json().catch(() => null)) as { detail?: string } | null
  return { error: body?.detail ?? 'Could not create the account.' }
}

export async function* streamChat(
  question: string,
  userEpisode: number,
): AsyncGenerator<ChatEvent> {
  const { data } = await supabase.auth.getSession()
  const accessToken = data.session?.access_token

  if (!accessToken) {
    yield { type: 'error', message: 'Your session expired. Please log in again.' }
    return
  }

  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${accessToken}`,
    },
    body: JSON.stringify({ question, user_episode: userEpisode }),
  })

  if (!response.ok || !response.body) {
    yield { type: 'error', message: 'Could not reach The Coordinate AI.' }
    return
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    buffer += decoder.decode(value, { stream: true })
    const events = buffer.split('\n\n')
    buffer = events.pop() ?? ''

    for (const rawEvent of events) {
      const line = rawEvent.split('\n').find((l) => l.startsWith('data: '))
      if (!line) continue
      yield JSON.parse(line.slice('data: '.length)) as ChatEvent
    }
  }
}
