import { useEffect, useRef, useState } from 'react'
import { useOutletContext } from 'react-router-dom'
import BriefingCard from '../components/chat/BriefingCard'
import ChatInput from '../components/chat/ChatInput'
import MessageList from '../components/chat/MessageList'
import type { Message } from '../components/chat/MessageBubble'
import type { LayoutContext } from '../components/layout/Layout'
import { streamChat } from '../lib/api'
import type { ChatSource } from '../types/chat'
import episodes from '../data/episodes.json'
import type { Episode } from '../types/episode'

const episodeList = episodes as Episode[]

function updateLastMessage(prev: Message[], updater: (message: Message) => Message): Message[] {
  const next = [...prev]
  next[next.length - 1] = updater(next[next.length - 1])
  return next
}

function Chat() {
  const { userEpisode } = useOutletContext<LayoutContext>()
  const currentEpisode = episodeList.find((episode) => episode.global_number === userEpisode)
  const progressLoaded = userEpisode !== null
  const [messages, setMessages] = useState<Message[]>([])
  const [isStreaming, setIsStreaming] = useState(false)
  const scrollRef = useRef<HTMLDivElement>(null)
  const stickToBottomRef = useRef(true)
  const smoothNextScrollRef = useRef(false)

  function handleScroll() {
    const el = scrollRef.current
    if (!el) return
    const distanceFromBottom = el.scrollHeight - el.scrollTop - el.clientHeight
    stickToBottomRef.current = distanceFromBottom < 80
  }

  useEffect(() => {
    if (!stickToBottomRef.current) return
    const behavior = smoothNextScrollRef.current ? 'smooth' : 'auto'
    smoothNextScrollRef.current = false
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior })
  }, [messages])

  async function handleSubmit(question: string) {
    if (userEpisode === null) return
    stickToBottomRef.current = true
    smoothNextScrollRef.current = true
    setMessages((prev) => [
      ...prev,
      { role: 'user', content: question },
      { role: 'assistant', content: '' },
    ])
    setIsStreaming(true)

    let pendingSources: ChatSource[] | undefined

    for await (const event of streamChat(question, userEpisode)) {
      if (event.type === 'sources') {
        pendingSources = event.sources
      } else if (event.type === 'token') {
        const { content } = event
        setMessages((prev) =>
          updateLastMessage(prev, (message) => ({
            ...message,
            content: message.content + content,
          })),
        )
      } else if (event.type === 'done') {
        const sources = pendingSources
        if (sources) {
          setMessages((prev) => updateLastMessage(prev, (message) => ({ ...message, sources })))
        }
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
      <div ref={scrollRef} onScroll={handleScroll} className="relative flex-1 overflow-y-auto">
        {currentEpisode && (
          <BriefingCard>
            <strong className="text-ash">
              Spoiler-safe through S{currentEpisode.season} · EP{' '}
              {String(currentEpisode.episode_in_season).padStart(2, '0')} — {currentEpisode.title}.
            </strong>{' '}
            Answers stay inside that point in the story — nothing from later episodes. Adjust your
            progress anytime with the selector, top right.
          </BriefingCard>
        )}
        <MessageList messages={messages} />
        <div
          aria-hidden="true"
          className="pointer-events-none sticky bottom-0 -mt-16 h-16 bg-gradient-to-t from-ink to-transparent"
        />
      </div>
      <ChatInput onSubmit={handleSubmit} disabled={isStreaming || !progressLoaded} />
    </div>
  )
}

export default Chat
