import { Navigate, Outlet, useOutletContext } from 'react-router-dom'
import { useAuth } from './useAuth'

function RequireAuth() {
  const { session, loading } = useAuth()
  const outletContext = useOutletContext()

  if (loading) return null
  if (!session) return <Navigate to="/login" replace />
  return <Outlet context={outletContext} />
}

export default RequireAuth
