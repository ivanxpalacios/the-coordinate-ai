import type { Session } from '@supabase/supabase-js'
import { createContext } from 'react'

export interface AuthContextValue {
  session: Session | null
  loading: boolean
  signIn: (email: string, password: string) => Promise<{ error: string | null }>
  signOut: () => Promise<void>
}

export const AuthContext = createContext<AuthContextValue | null>(null)
