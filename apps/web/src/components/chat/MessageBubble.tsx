import type { ChatSource } from '../../types/chat'

export interface Message {
  role: 'user' | 'assistant'
  content: string
  sources?: ChatSource[]
}

function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === 'user'

  if (isUser) {
    return (
      <div className="flex justify-end">
        <div className="max-w-xl rounded-2xl border border-line bg-panel px-4 py-2">
          <p className="text-sm text-ash">{message.content}</p>
        </div>
      </div>
    )
  }

  const primarySource = message.sources?.[0]

  return (
    <div className="flex justify-start">
      <div className="max-w-2xl text-left">
        <p className="whitespace-pre-wrap text-sm text-ash">{message.content}</p>
        {primarySource && (
          <a
            href={primarySource.source_url}
            target="_blank"
            rel="noreferrer"
            className="mt-1 inline-block font-mono text-xs text-fog underline decoration-line hover:text-signal"
          >
            source: {primarySource.source_title}
          </a>
        )}
      </div>
    </div>
  )
}

export default MessageBubble
