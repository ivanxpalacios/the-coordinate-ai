import { useState } from 'react'
import { Link, Outlet } from 'react-router-dom'
import EpisodeSelector from '../progress/EpisodeSelector'

export interface LayoutContext {
  userEpisode: number
}

function Layout() {
  const [userEpisode, setUserEpisode] = useState(9)

  return (
    <div className="flex h-svh flex-col">
      <nav className="flex items-center justify-between border-b border-line px-6 py-3">
        <Link to="/" className="font-display text-lg tracking-wide">
          THE COORDINATE AI
        </Link>
        <div className="flex items-center gap-4">
          <EpisodeSelector value={userEpisode} onChange={setUserEpisode} />
          <Link to="/about" className="font-mono text-sm text-fog hover:text-ash">
            About
          </Link>
        </div>
      </nav>

      <main className="min-h-0 flex-1">
        <Outlet context={{ userEpisode } satisfies LayoutContext} />
      </main>

      <footer className="border-t border-line px-6 py-3 text-center font-mono text-xs text-fog">
        Unofficial fan project. Not affiliated with Kodansha, MAPPA, or Wit Studio.
      </footer>
    </div>
  )
}

export default Layout
