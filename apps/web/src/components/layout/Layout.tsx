import { Link, Outlet } from 'react-router-dom'

function Layout() {
  return (
    <div className="flex min-h-svh flex-col">
      <nav className="flex items-center justify-between border-b border-zinc-800 px-6 py-4">
        <Link to="/" className="font-medium">
          The Coordinate AI
        </Link>
        <Link to="/about" className="text-sm text-zinc-400 hover:text-zinc-100">
          About
        </Link>
      </nav>

      <main className="flex-1">
        <Outlet />
      </main>

      <footer className="border-t border-zinc-800 px-6 py-4 text-center text-xs text-zinc-500">
        The Coordinate AI is an unofficial fan project. Not affiliated with Kodansha, MAPPA, or Wit Studio.
      </footer>
    </div>
  )
}

export default Layout
