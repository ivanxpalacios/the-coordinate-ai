import type { ReactNode } from 'react'

function BriefingCard({ children }: { children: ReactNode }) {
  return (
    <div className="relative mx-auto max-w-3xl px-6 py-6">
      <span className="absolute left-0 top-0 h-3 w-3 border-l border-t border-signal" />
      <span className="absolute right-0 top-0 h-3 w-3 border-r border-t border-signal" />
      <span className="absolute bottom-0 left-0 h-3 w-3 border-b border-l border-signal" />
      <span className="absolute bottom-0 right-0 h-3 w-3 border-b border-r border-signal" />
      <p className="font-mono text-xs uppercase tracking-wide text-fog">Briefing</p>
      <p className="mt-2 text-sm text-ash">{children}</p>
    </div>
  )
}

export default BriefingCard
