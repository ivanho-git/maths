import { motion } from 'framer-motion'

const POINTS = [
  {
    title: 'Global Network',
    body: 'Insights pulled from 180+ chapters across 38 countries, not just one office or one market.',
  },
  {
    title: 'Always Free',
    body: 'The newsletter, the toolkits, and the consulting itself stay free for every nonprofit we work with.',
  },
  {
    title: 'Practical Tools',
    body: 'Every issue ships at least one template or framework you can apply the same week.',
  },
  {
    title: 'Community-Built',
    body: 'Written by the volunteers running the projects — not a marketing team.',
  },
]

const GALLERY = [
  { label: 'Strategy workshop', tone: 'linear-gradient(135deg,#10192f,#2a3a63)' },
  { label: 'Chapter kickoff', tone: 'linear-gradient(135deg,#ff5a36,#ffb199)' },
  { label: 'Client presentation', tone: 'linear-gradient(135deg,#1c2944,#ff5a36)' },
  { label: 'Global summit', tone: 'linear-gradient(135deg,#ffb199,#10192f)' },
]

export default function Differentiators() {
  return (
    <section id="why" style={{ padding: '120px 0' }}>
      <div className="container-x">
        <p
          style={{
            fontSize: 14,
            fontWeight: 700,
            color: 'var(--ink-soft)',
            letterSpacing: 0.4,
            textTransform: 'uppercase',
            marginBottom: 16,
          }}
        >
          Why subscribe
        </p>
        <h2
          style={{
            fontSize: 'clamp(30px, 4.5vw, 48px)',
            fontWeight: 700,
            letterSpacing: -1.2,
            maxWidth: 680,
            marginBottom: 56,
          }}
        >
          What makes this newsletter different
        </h2>

        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
            gap: 40,
            marginBottom: 88,
          }}
        >
          {POINTS.map((point, i) => (
            <motion.div
              key={point.title}
              initial={{ opacity: 0, y: 24 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-10%' }}
              transition={{ duration: 0.55, delay: i * 0.08 }}
            >
              <h3 style={{ fontSize: 20, fontWeight: 700, margin: '0 0 10px', color: 'var(--ink)' }}>
                {point.title}
              </h3>
              <p style={{ fontSize: 15.5, lineHeight: 1.7, color: 'var(--ink-soft)', margin: 0 }}>
                {point.body}
              </p>
            </motion.div>
          ))}
        </div>

        <div
          id="chapters"
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
            gap: 20,
          }}
        >
          {GALLERY.map((g, i) => (
            <motion.div
              key={g.label}
              initial={{ opacity: 0, scale: 0.96 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true, margin: '-10%' }}
              transition={{ duration: 0.5, delay: i * 0.07 }}
              style={{
                aspectRatio: '4/3',
                borderRadius: 16,
                background: g.tone,
                display: 'flex',
                alignItems: 'flex-end',
                padding: 18,
              }}
            >
              <span style={{ color: '#fff', fontSize: 14, fontWeight: 600 }}>{g.label}</span>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
