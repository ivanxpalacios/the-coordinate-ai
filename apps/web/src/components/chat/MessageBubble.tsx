import ReactMarkdown, { type Components } from 'react-markdown'
import type { ChatSource } from '../../types/chat'

export interface Message {
  role: 'user' | 'assistant'
  content: string
  sources?: ChatSource[]
}

const markdownComponents: Components = {
  p: ({ children }) => <p className="text-sm text-ash [&:not(:first-child)]:mt-3">{children}</p>,
  strong: ({ children }) => <strong className="font-semibold text-ash">{children}</strong>,
  em: ({ children }) => <em className="italic text-ash">{children}</em>,
  ul: ({ children }) => <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-ash">{children}</ul>,
  ol: ({ children }) => <ol className="mt-2 list-decimal space-y-1 pl-5 text-sm text-ash">{children}</ol>,
  li: ({ children }) => <li className="text-sm text-ash">{children}</li>,
  a: ({ href, children }) => (
    <a
      href={href}
      target="_blank"
      rel="noreferrer"
      className="underline decoration-line hover:text-signal"
    >
      {children}
    </a>
  ),
  code: ({ children }) => (
    <code className="rounded bg-panel px-1 py-0.5 font-mono text-xs text-ash">{children}</code>
  ),
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
        {message.content ? (
          <ReactMarkdown components={markdownComponents}>{message.content}</ReactMarkdown>
        ) : (
          <span className="inline-block h-4 w-4 animate-pulse rounded-full bg-signal" />
        )}
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
