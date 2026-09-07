import { useEffect, useState } from 'react'
import { supabase } from '../../lib/supabase'
import { useAuth } from '../auth/useAuth'

export function useUserProgress() {
  const { session } = useAuth()
  const [userEpisode, setUserEpisodeState] = useState<number | null>(null)

  useEffect(() => {
    if (!session) return

    let cancelled = false

    async function loadProgress(userId: string) {
      const { data } = await supabase
        .from('user_progress')
        .select('last_episode')
        .eq('user_id', userId)
        .maybeSingle()

      if (cancelled) return

      if (data) {
        setUserEpisodeState(data.last_episode)
        return
      }

      const { data: created } = await supabase
        .from('user_progress')
        .insert({ user_id: userId })
        .select('last_episode')
        .single()

      if (!cancelled && created) setUserEpisodeState(created.last_episode)
    }

    loadProgress(session.user.id)
    return () => {
      cancelled = true
    }
  }, [session])

  async function setUserEpisode(episode: number) {
    setUserEpisodeState(episode)
    if (!session) return
    await supabase
      .from('user_progress')
      .update({ last_episode: episode, updated_at: new Date().toISOString() })
      .eq('user_id', session.user.id)
  }

  return { userEpisode: session ? userEpisode : null, setUserEpisode }
}
