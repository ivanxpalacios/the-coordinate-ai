import episodes from '../../data/episodes.json'
import type { Episode } from '../../types/episode'

const episodeList = episodes as Episode[]
const seasons = [...new Set(episodeList.map((episode) => episode.season))]

const TITLE_MAX_LENGTH = 28

function truncateTitle(title: string): string {
  if (title.length <= TITLE_MAX_LENGTH) return title
  return `${title.slice(0, TITLE_MAX_LENGTH).trimEnd()}…`
}

interface EpisodeSelectorProps {
  value: number
  onChange: (globalNumber: number) => void
}

function EpisodeSelector({ value, onChange }: EpisodeSelectorProps) {
  return (
    <select
      value={value}
      onChange={(event) => onChange(Number(event.target.value))}
      aria-label="Your progress"
      className="border border-line bg-panel px-2 py-0.5 font-mono text-xs text-fog focus:outline-none focus:text-ash"
    >
      {seasons.map((season) => (
        <optgroup key={season} label={`Season ${season}`}>
          {episodeList
            .filter((episode) => episode.season === season)
            .map((episode) => (
              <option key={episode.global_number} value={episode.global_number}>
                S{episode.season} · EP {String(episode.episode_in_season).padStart(2, '0')} —{' '}
                {truncateTitle(episode.title)}
              </option>
            ))}
        </optgroup>
      ))}
    </select>
  )
}

export default EpisodeSelector
