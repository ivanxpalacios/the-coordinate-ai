function Node({ label, sealed }: { label: string; sealed?: boolean }) {
  return (
    <div
      className={`border px-3 py-2 text-center text-xs text-ash ${
        sealed ? 'border-dashed border-sealed text-sealed' : 'border-line'
      }`}
    >
      {label}
    </div>
  )
}

function SystemMap() {
  return (
    <div className="font-mono text-xs">
      <div className="flex flex-wrap items-center gap-2">
        <Node label="React / Vite" />
        <span className="text-fog">— SSE →</span>
        <Node label="FastAPI" />
        <span className="text-fog">→</span>
        <Node label="Groq LLM" />
      </div>

      <div className="my-2 ml-8 h-6 border-l border-line" />

      <div className="flex flex-wrap items-center gap-2">
        <Node label="Neon · Postgres / pgvector" />
        <span className="text-fog">←</span>
        <Node label="Offline ETL pipeline" />
      </div>

      <div className="mt-4 flex flex-wrap items-center gap-2">
        <Node label="Supabase Auth — JWT verified" />
      </div>
    </div>
  )
}

export default SystemMap
