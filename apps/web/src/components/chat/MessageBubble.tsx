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

  return (
    <div className="flex justify-start">
      <div className="max-w-xl text-left">
        <p className="whitespace-pre-wrap text-sm text-ash">{message.content}</p>
        {message.sources && message.sources.length > 0 && (
          <ul className="mt-1 flex flex-wrap gap-x-3 font-mono text-xs text-fog">
            {message.sources.map((source) => (
              <li key={source.chunk_id}>source: {source.source_title}</li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}

export default MessageBubble
