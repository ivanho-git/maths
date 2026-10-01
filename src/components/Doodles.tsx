// Original hand-drawn-style doodles for 180 Degrees Consulting.
type P = { size?: number; style?: React.CSSProperties }

export function Megaphone({ size = 160, style }: P) {
  return (
    <svg width={size} height={size} viewBox="0 0 160 160" fill="none" style={style} aria-hidden>
      <path d="M30 70 L100 38 L104 122 L34 96 Z" fill="#fff" stroke="var(--ink)" strokeWidth="4" strokeLinejoin="round" />
      <path d="M100 38 C116 50 118 108 104 122" fill="var(--lilac)" stroke="var(--ink)" strokeWidth="4" />
      <rect x="18" y="68" width="18" height="30" rx="5" fill="var(--green)" stroke="var(--ink)" strokeWidth="4" />
      <path d="M44 100 L52 132 L66 128 L60 102" fill="#fff" stroke="var(--ink)" strokeWidth="4" strokeLinejoin="round" />
      <path d="M126 58 L144 48 M130 80 L150 80 M126 102 L144 112" stroke="var(--ink)" strokeWidth="4" strokeLinecap="round" />
    </svg>
  )
}

export function PaperPlane({ size = 140, style }: P) {
  return (
    <svg width={size} height={size} viewBox="0 0 140 140" fill="none" style={style} aria-hidden>
      <path d="M14 66 L126 20 L92 120 L66 84 Z" fill="#fff" stroke="var(--ink)" strokeWidth="4" strokeLinejoin="round" />
      <path d="M66 84 L126 20 L58 108 Z" fill="var(--green)" stroke="var(--ink)" strokeWidth="4" strokeLinejoin="round" />
      <path d="M10 112 C24 100 30 118 44 106" stroke="var(--ink)" strokeWidth="3.5" strokeLinecap="round" strokeDasharray="2 9" />
    </svg>
  )
}

const L = { stroke: 'var(--ink)', strokeWidth: 3.5, strokeLinecap: 'round' as const, strokeLinejoin: 'round' as const }

export function Sparkle({ size = 46, style }: P) {
  return (
    <svg width={size} height={size} viewBox="0 0 46 46" fill="none" style={style} aria-hidden>
      <path d="M23 4 C25 17 29 21 42 23 C29 25 25 29 23 42 C21 29 17 25 4 23 C17 21 21 17 23 4Z" fill="#fff" {...L} />
    </svg>
  )
}

export function HeartBubble({ size = 90, style }: P) {
  return (
    <svg width={size} height={size} viewBox="0 0 90 90" fill="none" style={style} aria-hidden>
      <path d="M14 12 h62 a8 8 0 0 1 8 8 v34 a8 8 0 0 1 -8 8 h-34 l-16 14 v-14 h-12 a8 8 0 0 1 -8 -8 v-34 a8 8 0 0 1 8 -8z" fill="#fff" {...L} />
      <path d="M45 50 C30 40 32 26 41 28 C44 29 45 32 45 33 C45 32 46 29 49 28 C58 26 60 40 45 50Z" fill="var(--green)" {...L} />
    </svg>
  )
}

export function Pencil({ size = 90, style }: P) {
  return (
    <svg width={size} height={size} viewBox="0 0 90 90" fill="none" style={style} aria-hidden>
      <path d="M20 70 L62 18 L74 28 L32 80 L16 84Z" fill="var(--lilac)" {...L} />
      <path d="M62 18 L68 11 L80 21 L74 28" fill="#fff" {...L} />
      <path d="M20 70 L32 80" {...L} />
    </svg>
  )
}

export function Mug({ size = 80, style }: P) {
  return (
    <svg width={size} height={size} viewBox="0 0 80 80" fill="none" style={style} aria-hidden>
      <path d="M14 30 h40 v26 a12 12 0 0 1 -12 12 h-16 a12 12 0 0 1 -12 -12z" fill="#fff" {...L} />
      <path d="M54 36 h6 a8 8 0 0 1 0 16 h-6" {...L} />
      <path d="M26 22 c-4 -6 4 -8 0 -14 M38 22 c-4 -6 4 -8 0 -14" {...L} />
      <path d="M22 44 h24" stroke="var(--green)" strokeWidth="6" strokeLinecap="round" />
    </svg>
  )
}

export function Globe({ size = 84, style }: P) {
  return (
    <svg width={size} height={size} viewBox="0 0 84 84" fill="none" style={style} aria-hidden>
      <circle cx="42" cy="42" r="30" fill="var(--green)" {...L} />
      <path d="M14 34 C30 40 54 30 70 36 M16 54 C32 48 52 58 68 50" stroke="#fff" strokeWidth="3.5" strokeLinecap="round" />
      <ellipse cx="42" cy="42" rx="12" ry="30" {...L} />
    </svg>
  )
}

/** Hand-painted marker highlight; place behind a word. */
export function BrushStroke({ color = 'var(--green)', style }: { color?: string; style?: React.CSSProperties }) {
  return (
    <svg viewBox="0 0 400 100" preserveAspectRatio="none" style={{ position: 'absolute', top: '4%', left: '-10%', width: '120%', height: '100%', zIndex: -1, ...style }} aria-hidden>
      <path d="M8 22 C80 8 200 14 392 6 C396 40 388 66 394 92 C260 86 120 98 6 90 C12 64 2 44 8 22Z" fill={color} />
    </svg>
  )
}
