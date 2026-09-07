import { useState, type FormEvent } from 'react'

interface ChatInputProps {
  onSubmit: (question: string) => void
  disabled?: boolean
}

function ChatInput({ onSubmit, disabled = false }: ChatInputProps) {
  const [value, setValue] = useState('')

  function handleSubmit(event: FormEvent) {
    event.preventDefault()
    if (!value.trim() || disabled) return
    onSubmit(value)
    setValue('')
  }

  return (
    <div className="px-6 py-4">
      <form
        onSubmit={handleSubmit}
        className="mx-auto flex max-w-2xl items-center gap-2 rounded-full border border-line bg-panel py-2 pl-5 pr-2"
      >
        <input
          type="text"
          value={value}
          onChange={(event) => setValue(event.target.value)}
          disabled={disabled}
          placeholder="Ask about the story so far…"
          className="flex-1 bg-transparent text-sm text-ash placeholder:text-fog focus:outline-none disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={!value.trim() || disabled}
          aria-label="Send"
          className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-signal text-ink transition-opacity disabled:opacity-30"
        >
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            className="h-4 w-4"
            aria-hidden="true"
          >
            <path d="M12 19V5" />
            <path d="M5 12l7-7 7 7" />
          </svg>
        </button>
      </form>
    </div>
  )
}

export default ChatInput
