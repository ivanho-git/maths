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
