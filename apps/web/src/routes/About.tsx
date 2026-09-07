import { Link } from 'react-router-dom'
import DefenseLayers from '../components/about/DefenseLayers'
import SystemMap from '../components/about/SystemMap'

interface StackRow {
  layer: string
  tech: string
  status: 'live' | 'todo'
  note: string
}

const stack: StackRow[] = [
  { layer: 'Frontend', tech: 'Vite · React · TypeScript · Tailwind', status: 'live', note: 'this page' },
  { layer: 'Backend', tech: 'FastAPI · Python 3.12', status: 'live', note: '/chat streams over SSE' },
  { layer: 'Vector store', tech: 'Neon Postgres + pgvector', status: 'live', note: '~786 chunks ingested' },
  { layer: 'LLM', tech: 'Groq', status: 'live', note: 'free tier' },
  { layer: 'Auth & progress', tech: 'Supabase Auth', status: 'todo', note: 'Phase 4' },
  { layer: 'Deployment', tech: 'Vercel + Oracle Cloud', status: 'todo', note: 'Phase 6' },
]

function About() {
  return (
    <div className="h-full overflow-y-auto">
      <div className="mx-auto max-w-3xl px-6 py-10">
        <section>
          <h1 className="font-display text-3xl tracking-wide text-ash">The Coordinate AI</h1>
          <p className="mt-3 text-sm text-ash">
            Ask anything about the Attack on Titan story so far — get answers built only from
            what your declared episode should already know, sources cited, nothing from later
            arcs.
          </p>
          <p className="mt-4 font-mono text-xs text-fog">
            Unofficial, non-commercial fan project — not affiliated with Kodansha, MAPPA, or Wit
            Studio. Text sourced from wiki content under CC BY-SA, always attributed.
          </p>
          <Link
            to="/"
            className="mt-6 inline-block rounded-full bg-signal px-5 py-2 font-mono text-xs uppercase tracking-wide text-ink"
          >
            Start asking →
          </Link>
          <p className="mt-4 font-mono text-xs text-fog">
            Built by Iván Palacios —{' '}
            <a href="https://github.com/ivanxpalacios" className="hover:text-ash" target="_blank" rel="noreferrer">
              GitHub
            </a>{' '}
            ·{' '}
            <a href="https://www.linkedin.com/in/ivanpalaciosdev/" className="hover:text-ash" target="_blank" rel="noreferrer">
              LinkedIn
            </a>{' '}
            ·{' '}
            <a href="https://ivanpalacios.dev/" className="hover:text-ash" target="_blank" rel="noreferrer">
              Portfolio
            </a>
          </p>
        </section>

        <hr className="my-8 border-line" />

        <section>
          <h2 className="font-mono text-xs text-fog">01 — The problem</h2>
          <p className="mt-2 text-sm text-ash">
            Halfway through Attack on Titan, every search engine, wiki, and forum is a minefield.
            Ask the wrong question and you'll know who dies before you get there. The Coordinate
            AI answers lore questions using only what you should already know, based on the
            episode you've declared — nothing from later arcs ever reaches the answer.
          </p>
        </section>

        <hr className="my-8 border-line" />

        <section>
          <h2 className="font-mono text-xs text-fog">02 — How it stays spoiler-free</h2>
          <p className="mt-2 text-sm text-ash">
            Four independent layers, so a failure in one doesn't leak a spoiler on its own.
          </p>
          <div className="mt-4">
            <DefenseLayers />
          </div>
        </section>

        <hr className="my-8 border-line" />

        <section>
          <h2 className="font-mono text-xs text-fog">03 — System map</h2>
          <p className="mt-2 text-sm text-ash">
            A question is embedded, filtered by episode, reranked, and answered — streamed back
            token by token.
          </p>
          <div className="mt-4">
            <SystemMap />
          </div>
        </section>

        <hr className="my-8 border-line" />

        <section>
          <h2 className="font-mono text-xs text-fog">04 — Scope &amp; stack</h2>
          <p className="mt-2 text-sm text-ash">
            MVP is spoiler-free chat, episode progress, and auth — English only. Sources are wiki
            content under CC BY-SA, always cited.
          </p>
          <table className="mt-4 w-full border-collapse text-left font-mono text-xs">
            <tbody>
              {stack.map((row) => (
                <tr key={row.layer} className="border-t border-line">
                  <td className="py-2 pr-3 text-fog">{row.layer}</td>
                  <td className="py-2 pr-3 text-ash">{row.tech}</td>
                  <td className={`py-2 ${row.status === 'todo' ? 'text-sealed' : 'text-fog'}`}>
                    {row.status === 'todo' ? `TODO — ${row.note}` : row.note}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      </div>
    </div>
  )
}

export default About
