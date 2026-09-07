import MessageBubble, { type Message } from './MessageBubble'

function MessageList({ messages }: { messages: Message[] }) {
  return (
    <div className="mx-auto flex max-w-2xl flex-col gap-6 px-6 py-6">
      {messages.map((message, index) => (
        <MessageBubble key={index} message={message} />
      ))}
    </div>
  )
}

export default MessageList
