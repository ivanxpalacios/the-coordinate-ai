import { Navigate, Outlet } from 'react-router-dom'
import { useAuth } from './useAuth'

function RequireAuth() {
  const { session, loading } = useAuth()

  if (loading) return null
  if (!session) return <Navigate to="/login" replace />
  return <Outlet />
}

export default RequireAuth
