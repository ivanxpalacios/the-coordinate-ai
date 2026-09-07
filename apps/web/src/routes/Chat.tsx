import BriefingCard from '../components/chat/BriefingCard'
import ChatInput from '../components/chat/ChatInput'
import MessageList from '../components/chat/MessageList'
import type { Message } from '../components/chat/MessageBubble'

const mockMessages: Message[] = [
  { role: 'user', content: 'Who is the Female Titan?' },
  {
    role: 'assistant',
    content:
      "She's one of the Titans that infiltrated the Scout Regiment during the 57th expedition beyond the walls.",
    source: 'aot.fandom.com/wiki/Female_Titan',
  },
]

function Chat() {
  return (
    <div className="flex h-full flex-col">
      <div className="relative flex-1 overflow-y-auto">
        <BriefingCard>
          You're marked through Episode 9. Ask about arcs, characters, or titans —
          I won't go past your line.
        </BriefingCard>
        <MessageList messages={mockMessages} />
        <div
          aria-hidden="true"
          className="sticky bottom-0 -mt-16 h-16 bg-gradient-to-t from-ink to-transparent"
        />
      </div>
      <ChatInput />
    </div>
  )
}

export default Chat
