import { Link, Outlet } from 'react-router-dom'

function Layout() {
  return (
    <div className="flex h-svh flex-col">
      <nav className="flex items-center justify-between border-b border-line px-6 py-3">
        <Link to="/" className="font-display text-lg tracking-wide">
          THE COORDINATE AI
        </Link>
        <div className="flex items-center gap-4">
          <span className="border border-line px-2 py-0.5 font-mono text-xs text-fog">
            S1 · EP 09
          </span>
          <Link to="/about" className="font-mono text-sm text-fog hover:text-ash">
            About
          </Link>
        </div>
      </nav>

      <main className="min-h-0 flex-1">
        <Outlet />
      </main>

      <footer className="border-t border-line px-6 py-3 text-center font-mono text-xs text-fog">
        Unofficial fan project. Not affiliated with Kodansha, MAPPA, or Wit Studio.
      </footer>
    </div>
  )
}

export default Layout
