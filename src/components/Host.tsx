import { motion } from 'framer-motion'

// Original loose-ink character for 180 Degrees Consulting:
// a student with short curly hair and round glasses, holding up a newsletter.
type P = { size?: number; style?: React.CSSProperties }

const ink = { stroke: 'var(--ink)', strokeWidth: 5, strokeLinecap: 'round' as const, strokeLinejoin: 'round' as const, fill: 'none' }

function Draw({ d, delay = 0, ...rest }: { d: string; delay?: number } & React.SVGProps<SVGPathElement>) {
  return (
    <motion.path
      d={d}
      initial={{ pathLength: 0 }}
      whileInView={{ pathLength: 1 }}
      viewport={{ once: true }}
      transition={{ duration: 1.1, delay, ease: 'easeInOut' }}
      {...ink}
      {...(rest as object)}
    />
  )
}

export function Host({ size = 300, style }: P) {
  return (
    <motion.svg
      width={size}
      height={size * 1.15}
      viewBox="0 0 300 345"
      style={style}
      aria-hidden
      initial={{ y: 30, opacity: 0 }}
      whileInView={{ y: 0, opacity: 1 }}
      viewport={{ once: true }}
      transition={{ duration: 0.7 }}
    >
      {/* body */}
      <path d="M78 345 C70 270 92 222 150 218 C208 222 232 270 222 345Z" fill="#fff" stroke="none" />
      <Draw d="M78 345 C70 270 92 222 150 218 C208 222 232 270 222 345" delay={0.1} />
      {/* green scarf */}
      <path d="M118 222 C132 240 168 240 182 222 C186 236 176 252 150 254 C124 252 114 236 118 222Z" fill="var(--green)" stroke="var(--ink)" strokeWidth="5" strokeLinejoin="round" />
      {/* neck */}
      <Draw d="M136 196 L134 222 M164 196 L166 222" delay={0.2} />
      {/* head */}
      <path d="M96 128 C92 72 124 50 152 50 C186 50 210 78 206 128 C202 178 180 202 150 202 C120 202 100 178 96 128Z" fill="#fff" stroke="none" />
      <Draw d="M96 128 C92 72 124 50 152 50 C186 50 210 78 206 128 C202 178 180 202 150 202 C120 202 100 178 96 128Z" delay={0.25} />
      {/* curly hair */}
      <path
        d="M92 112 C80 96 90 74 106 74 C100 52 124 36 142 46 C150 26 182 30 186 50 C204 42 222 62 212 80 C228 90 222 116 206 116 C200 96 186 86 170 90 C160 78 138 78 130 90 C116 84 100 96 102 116Z"
        fill="var(--ink)"
        stroke="var(--ink)"
        strokeWidth="4"
        strokeLinejoin="round"
      />
      {/* glasses */}
      <Draw d="M116 132 a16 16 0 1 0 32 0 a16 16 0 1 0 -32 0 M156 132 a16 16 0 1 0 32 0 a16 16 0 1 0 -32 0 M148 130 h8" delay={0.6} strokeWidth={4} />
      <circle cx="132" cy="134" r="3.5" fill="var(--ink)" />
      <circle cx="172" cy="134" r="3.5" fill="var(--ink)" />
      {/* nose + smile */}
      <Draw d="M152 146 C146 156 150 162 158 160" delay={0.8} strokeWidth={4} />
      <Draw d="M134 174 C144 186 164 186 174 172" delay={0.9} strokeWidth={4} />
      {/* arms holding the newsletter */}
      <Draw d="M94 262 C66 250 64 216 86 196" delay={0.4} />
      <Draw d="M206 262 C234 250 236 216 214 196" delay={0.4} />
      {/* newsletter sheet */}
      <motion.g initial={{ rotate: -8, y: 10 }} whileInView={{ rotate: -4, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.8, delay: 0.5 }} style={{ originX: '150px', originY: '200px' }}>
        <path d="M70 160 L230 150 L238 246 L78 258Z" fill="#fff" stroke="var(--ink)" strokeWidth="5" strokeLinejoin="round" />
        <path d="M92 178 L150 174" stroke="var(--green)" strokeWidth="12" strokeLinecap="round" />
        <path d="M92 202 L214 194 M94 220 L200 212 M96 236 L176 230" stroke="var(--ink)" strokeWidth="4" strokeLinecap="round" />
      </motion.g>
      {/* hands */}
      <path d="M72 186 c-10 4 -10 18 2 20 c10 2 18 -8 12 -18Z" fill="#fff" stroke="var(--ink)" strokeWidth="4.5" />
      <path d="M228 176 c10 4 10 18 -2 20 c-10 2 -18 -8 -12 -18Z" fill="#fff" stroke="var(--ink)" strokeWidth="4.5" />
    </motion.svg>
  )
}
