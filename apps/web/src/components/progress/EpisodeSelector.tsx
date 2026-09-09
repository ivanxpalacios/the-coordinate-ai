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
  disabled?: boolean
  showNames: boolean
  onToggleShowNames: (value: boolean) => void
}

function EpisodeSelector({
  value,
  onChange,
  disabled = false,
  showNames,
  onToggleShowNames,
}: EpisodeSelectorProps) {
  return (
    <div className="flex items-center gap-2">
      <label className="flex items-center gap-1 font-mono text-xs text-fog">
        <input
          type="checkbox"
          checked={showNames}
          onChange={(event) => onToggleShowNames(event.target.checked)}
          className="h-3.5 w-3.5 accent-signal"
        />
        Show Episode Names
      </label>
      <select
        value={value}
        onChange={(event) => onChange(Number(event.target.value))}
        disabled={disabled}
        aria-label="Your progress"
        style={{
          width: showNames ? `min(55vw, ${TITLE_MAX_LENGTH + 20}ch)` : '24ch',
        }}
        className="overflow-hidden text-ellipsis whitespace-nowrap border border-line bg-panel px-2 py-0.5 font-mono text-xs text-fog focus:outline-none focus:text-ash disabled:opacity-50"
      >
        {seasons.map((season) => (
          <optgroup key={season} label={`Season ${season}`}>
            {episodeList
              .filter((episode) => episode.season === season)
              .map((episode) => (
                <option key={episode.global_number} value={episode.global_number}>
                  #{episode.global_number} · S{episode.season} · EP{' '}
                  {String(episode.episode_in_season).padStart(2, '0')}
                  {showNames ? ` — ${truncateTitle(episode.title)}` : ''}
                </option>
              ))}
          </optgroup>
        ))}
      </select>
    </div>
  )
}

export default EpisodeSelector
