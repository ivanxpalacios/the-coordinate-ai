export interface Message {
  role: 'user' | 'assistant'
  content: string
  source?: string
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
        <p className="text-sm text-ash">{message.content}</p>
        {message.source && (
          <p className="mt-1 font-mono text-xs text-fog">source: {message.source}</p>
        )}
      </div>
    </div>
  )
}

export default MessageBubble
