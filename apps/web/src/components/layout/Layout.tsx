import { Link, Outlet } from 'react-router-dom'

function Layout() {
  return (
    <div className="flex min-h-svh flex-col">
      <nav className="flex items-center justify-between border-b border-line px-6 py-3">
        <Link to="/" className="font-display text-lg tracking-wide">
          THE COORDINATE AI
        </Link>
        <Link to="/about" className="font-mono text-sm text-fog hover:text-ash">
          About
        </Link>
      </nav>

      <main className="flex-1">
        <Outlet />
      </main>

      <footer className="border-t border-line px-6 py-3 text-center font-mono text-xs text-fog">
        Unofficial fan project. Not affiliated with Kodansha, MAPPA, or Wit Studio.
      </footer>
    </div>
  )
}

export default Layout
