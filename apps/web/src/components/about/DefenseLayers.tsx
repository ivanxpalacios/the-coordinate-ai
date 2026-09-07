interface Layer {
  label: string
  description: string
  primary?: boolean
}

const layers: Layer[] = [
  {
    label: 'Retrieval filter',
    description: 'reveal_episode ≤ user_episode, enforced in the vector query itself.',
    primary: true,
  },
  {
    label: 'System prompt',
    description: 'Explicit instruction not to speculate beyond the retrieved context.',
  },
  {
    label: 'Neutral refusal',
    description: "A generic non-answer when there's no in-scope context — never a tell.",
  },
  {
    label: 'Adversarial suite',
    description: 'Trap questions per episode level, run on every change in CI.',
  },
]

function DefenseLayers() {
  return (
    <ol className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      {layers.map((layer, index) => (
        <li
          key={layer.label}
          className={`border px-4 py-3 ${layer.primary ? 'border-signal' : 'border-line'}`}
        >
          <span className="font-mono text-xs text-fog">
            {String(index + 1).padStart(2, '0')}
          </span>
          <p className="mt-1 text-sm text-ash">{layer.label}</p>
          <p className="mt-1 text-xs text-fog">{layer.description}</p>
        </li>
      ))}
    </ol>
  )
}

export default DefenseLayers
