// Original hand-drawn-style characters for 180 Degrees Consulting.
type P = { size?: number; style?: React.CSSProperties }
const S = { stroke: 'var(--ink)', strokeWidth: 4, strokeLinecap: 'round' as const, strokeLinejoin: 'round' as const }

/** Student consultant striding forward, holding a clipboard. */
export function Strider({ size = 320, style }: P) {
  return (
    <svg width={size} height={size * 1.25} viewBox="0 0 240 300" fill="none" style={style} aria-hidden>
      <path d="M96 196 L70 262 L46 268" {...S} />
      <path d="M128 196 L150 254 L178 256" {...S} />
      <path d="M40 270 q8 -10 22 -4" {...S} fill="var(--ink)" />
      <path d="M172 258 q12 -10 22 0 l-4 6 h-20z" {...S} fill="var(--ink)" />
      <path d="M84 110 Q82 196 98 204 L134 204 Q150 190 142 110 Q114 92 84 110Z" fill="#fff" {...S} />
      <path d="M90 128 Q60 150 52 176" {...S} />
      <path d="M138 126 Q170 136 182 118" {...S} />
      <rect x="168" y="84" width="40" height="52" rx="4" fill="var(--green)" {...S} transform="rotate(14 188 110)" />
      <path d="M178 100 h20 M176 110 h22 M174 120 h16" stroke="#fff" strokeWidth="3" strokeLinecap="round" transform="rotate(14 188 110)" />
      <circle cx="112" cy="72" r="28" fill="#fff" {...S} />
      <path d="M86 64 Q90 34 118 40 Q146 44 140 72 Q132 52 112 56 Q96 58 86 64Z" fill="var(--ink)" {...S} />
      <circle cx="104" cy="76" r="3" fill="var(--ink)" />
      <circle cx="122" cy="76" r="3" fill="var(--ink)" />
      <path d="M104 88 Q113 95 122 88" {...S} />
    </svg>
  )
}

/** Person sitting cross-legged, reading the newsletter on a laptop. */
export function Reader({ size = 220, style }: P) {
  return (
    <svg width={size} height={size} viewBox="0 0 220 220" fill="none" style={style} aria-hidden>
      <path d="M40 186 Q110 150 180 186 Q110 206 40 186Z" fill="var(--lilac)" {...S} />
      <path d="M78 176 Q72 110 110 104 Q148 110 142 176Z" fill="#fff" {...S} />
      <rect x="74" y="140" width="72" height="44" rx="5" fill="var(--ink)" {...S} />
      <circle cx="110" cy="158" r="7" fill="var(--green)" />
      <circle cx="110" cy="76" r="24" fill="#fff" {...S} />
      <path d="M86 70 Q92 46 116 50 Q138 56 132 78 Q120 58 100 66Z" fill="var(--green)" {...S} />
      <path d="M100 82 h6 M114 82 h6" {...S} />
    </svg>
  )
}

/** Waving figure with a speech bubble. */
export function Waver({ size = 200, style }: P) {
  return (
    <svg width={size} height={size} viewBox="0 0 200 200" fill="none" style={style} aria-hidden>
      <path d="M120 22 h62 a10 10 0 0 1 10 10 v26 a10 10 0 0 1 -10 10 h-36 l-14 12 v-12 h-12 a10 10 0 0 1 -10 -10 v-26 a10 10 0 0 1 10 -10z" fill="#fff" {...S} />
      <path d="M132 44 h44" {...S} />
      <path d="M62 188 Q58 120 86 112 Q116 116 112 188Z" fill="var(--green)" {...S} />
      <path d="M68 132 Q40 110 44 82" {...S} />
      <path d="M38 78 l6 -10 l6 10" {...S} />
      <circle cx="86" cy="84" r="22" fill="#fff" {...S} />
      <path d="M64 80 Q70 58 92 62 Q110 68 106 86 Q96 70 78 76Z" fill="var(--ink)" {...S} />
      <path d="M80 92 Q86 98 94 92" {...S} />
    </svg>
  )
}
