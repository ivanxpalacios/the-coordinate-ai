import { useState } from 'react'
import { useOutletContext } from 'react-router-dom'
import BriefingCard from '../components/chat/BriefingCard'
import ChatInput from '../components/chat/ChatInput'
import MessageList from '../components/chat/MessageList'
import type { Message } from '../components/chat/MessageBubble'
import type { LayoutContext } from '../components/layout/Layout'
import { streamChat } from '../lib/api'

function updateLastMessage(prev: Message[], updater: (message: Message) => Message): Message[] {
  const next = [...prev]
  next[next.length - 1] = updater(next[next.length - 1])
  return next
}

function Chat() {
  const { userEpisode } = useOutletContext<LayoutContext>()
  const [messages, setMessages] = useState<Message[]>([])
  const [isStreaming, setIsStreaming] = useState(false)

  async function handleSubmit(question: string) {
    setMessages((prev) => [
      ...prev,
      { role: 'user', content: question },
      { role: 'assistant', content: '' },
    ])
    setIsStreaming(true)

    for await (const event of streamChat(question, userEpisode)) {
      if (event.type === 'sources') {
        const { sources } = event
        setMessages((prev) => updateLastMessage(prev, (message) => ({ ...message, sources })))
      } else if (event.type === 'token') {
        const { content } = event
        setMessages((prev) =>
          updateLastMessage(prev, (message) => ({
            ...message,
            content: message.content + content,
          })),
        )
      } else if (event.type === 'error') {
        const { message: errorMessage } = event
        setMessages((prev) =>
          updateLastMessage(prev, (message) => ({ ...message, content: errorMessage })),
        )
      }
    }

    setIsStreaming(false)
  }

  return (
    <div className="flex h-full flex-col">
      <div className="relative flex-1 overflow-y-auto">
        <BriefingCard>
          You're marked through Episode {userEpisode}. Ask about arcs, characters, or titans —
          I won't go past your line.
        </BriefingCard>
        <MessageList messages={messages} />
        <div
          aria-hidden="true"
          className="sticky bottom-0 -mt-16 h-16 bg-gradient-to-t from-ink to-transparent"
        />
      </div>
      <ChatInput onSubmit={handleSubmit} disabled={isStreaming} />
    </div>
  )
}

export default Chat
