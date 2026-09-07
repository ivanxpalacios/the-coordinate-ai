import { useState, type FormEvent } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../features/auth/useAuth'
import { registerUser } from '../lib/api'

function Register() {
  const { signIn } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [accessCode, setAccessCode] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit(event: FormEvent) {
    event.preventDefault()
    setSubmitting(true)
    setError(null)

    const { error: registerError } = await registerUser(email, password, accessCode)
    if (registerError) {
      setError(registerError)
      setSubmitting(false)
      return
    }

    const { error: signInError } = await signIn(email, password)
    if (signInError) {
      setError(signInError)
      setSubmitting(false)
      return
    }
    navigate('/')
  }

  return (
    <div className="mx-auto flex h-full max-w-sm flex-col justify-center px-6">
      <h1 className="font-display text-2xl text-ash">Register</h1>
      <p className="mt-1 font-mono text-xs text-fog">Invite-only — you'll need an access code.</p>
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
          placeholder="Password (min. 8 characters)"
          minLength={8}
          required
          className="border border-line bg-panel px-3 py-2 text-sm text-ash placeholder:text-fog focus:outline-none"
        />
        <input
          type="text"
          value={accessCode}
          onChange={(event) => setAccessCode(event.target.value)}
          placeholder="Access code"
          required
          className="border border-line bg-panel px-3 py-2 text-sm text-ash placeholder:text-fog focus:outline-none"
        />
        {error && <p className="font-mono text-xs text-sealed">{error}</p>}
        <button
          type="submit"
          disabled={submitting}
          className="mt-2 rounded-full bg-signal px-5 py-2 font-mono text-xs uppercase tracking-wide text-ink disabled:opacity-50"
        >
          {submitting ? 'Creating account…' : 'Create account'}
        </button>
      </form>
      <p className="mt-4 font-mono text-xs text-fog">
        Already have an account? <Link to="/login" className="text-ash underline">Log in</Link>
      </p>
    </div>
  )
}

export default Register
