import { useEffect, useState } from 'react'
import { Link, Outlet, useNavigate } from 'react-router-dom'
import { useAuth } from '../../features/auth/useAuth'
import { useUserProgress } from '../../features/progress/useUserProgress'
import EpisodeSelector from '../progress/EpisodeSelector'

export interface LayoutContext {
  userEpisode: number | null
  showEpisodeNames: boolean
}

const SHOW_EPISODE_NAMES_STORAGE_KEY = 'episodeSelector.showNames'

function readStoredShowEpisodeNames(): boolean {
  const stored = window.localStorage.getItem(SHOW_EPISODE_NAMES_STORAGE_KEY)
  return stored === null ? true : stored === 'true'
}

function Layout() {
  const { session, signOut } = useAuth()
  const { userEpisode, setUserEpisode } = useUserProgress()
  const [showEpisodeNames, setShowEpisodeNames] = useState(readStoredShowEpisodeNames)
  const navigate = useNavigate()

  useEffect(() => {
    window.localStorage.setItem(SHOW_EPISODE_NAMES_STORAGE_KEY, String(showEpisodeNames))
  }, [showEpisodeNames])

  async function handleSignOut() {
    await signOut()
    navigate('/')
  }

  return (
    <div className="flex h-svh flex-col">
      <nav className="flex flex-wrap items-center justify-between gap-y-2 border-b border-line px-4 py-3 sm:px-6">
        <Link to="/" className="font-display text-lg tracking-wide">
          THE COORDINATE AI
        </Link>
        <div className="flex items-center gap-4">
          {session && (
            <EpisodeSelector
              value={userEpisode ?? 1}
              onChange={setUserEpisode}
              disabled={userEpisode === null}
              showNames={showEpisodeNames}
              onToggleShowNames={setShowEpisodeNames}
            />
          )}
          <Link to="/about" className="font-mono text-sm text-fog hover:text-ash">
            About
          </Link>
          {session ? (
            <button
              type="button"
              onClick={handleSignOut}
              className="font-mono text-sm text-fog hover:text-ash"
            >
              Log out
            </button>
          ) : (
            <Link to="/login" className="font-mono text-sm text-fog hover:text-ash">
              Log in
            </Link>
          )}
        </div>
      </nav>

      <main className="min-h-0 flex-1">
        <Outlet context={{ userEpisode, showEpisodeNames } satisfies LayoutContext} />
      </main>

      <footer className="border-t border-line px-6 py-3 text-center font-mono text-xs text-fog">
        Unofficial fan project. Not affiliated with Kodansha, MAPPA, or Wit Studio.
      </footer>
    </div>
  )
}

export default Layout
