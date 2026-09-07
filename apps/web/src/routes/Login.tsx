import { useEffect, useState, type FormEvent } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../features/auth/useAuth'

function Login() {
  const { session, signIn } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    if (session) navigate('/')
  }, [session, navigate])

  async function handleSubmit(event: FormEvent) {
    event.preventDefault()
    setSubmitting(true)
    setError(null)

    const { error } = await signIn(email, password)
    if (error) {
      setError(error)
      setSubmitting(false)
    }
  }

  return (
    <div className="mx-auto flex h-full max-w-sm flex-col justify-center px-6">
      <h1 className="font-display text-2xl text-ash">Log in</h1>
      <form onSubmit={handleSubmit} className="mt-6 flex flex-col gap-3">
        <input
          type="email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          placeholder="Email"
          required
          className="border border-line bg-panel px-3 py-2 text-sm text-ash placeholder:text-fog focus:outline-none"
        />
        <input
          type="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          placeholder="Password"
          required
          className="border border-line bg-panel px-3 py-2 text-sm text-ash placeholder:text-fog focus:outline-none"
        />
        {error && <p className="font-mono text-xs text-sealed">{error}</p>}
        <button
          type="submit"
          disabled={submitting}
          className="mt-2 rounded-full bg-signal px-5 py-2 font-mono text-xs uppercase tracking-wide text-ink disabled:opacity-50"
        >
          {submitting ? 'Logging in…' : 'Log in'}
        </button>
      </form>
      <p className="mt-4 font-mono text-xs text-fog">
        No account? <Link to="/register" className="text-ash underline">Register</Link>
      </p>
    </div>
  )
}

export default Login
