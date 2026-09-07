export interface Episode {
  global_number: number
  season: number
  episode_in_season: number
  title: string
  wiki_title: string | null
  arc: string
  manga_chapters: number[]
}
