import { useEffect, useRef, useState } from 'react'
import { motion, useInView } from 'framer-motion'

const ITEMS = [
  {
    index: '1.',
    kicker: 'Real projects, real outcomes',
    title: 'Impact Stories',
    body: "Deep dives into recently wrapped consulting engagements — the brief the chapter received, the strategy the student team built, and the measurable change it created for the nonprofit or social enterprise.",
    gradient: 'linear-gradient(135deg, #10192f 0%, #1c2944 55%, #ff5a36 150%)',
  },
  {
    index: '2.',
    kicker: 'News from 38 countries',
    title: 'Chapter Spotlights',
    body: "A rotating look at university chapters around the globe: new partnerships, recruitment drives, leadership transitions, and the local causes each team is rallying behind this term.",
    gradient: 'linear-gradient(135deg, #ff5a36 0%, #ffb199 55%, #10192f 150%)',
  },
  {
    index: '3.',
    kicker: 'Frameworks you can reuse',
    title: 'Resources & Toolkits',
    body: "Hand-picked consulting frameworks, discovery-call scripts, and stakeholder-mapping templates that our own teams rely on — simplified so any volunteer or nonprofit leader can put them to use.",
    gradient: 'linear-gradient(135deg, #1c2944 0%, #10192f 55%, #ffb199 150%)',
  },
]

function CoverageRow({
  item,
  onActive,
}: {
  item: (typeof ITEMS)[number]
  onActive: () => void
}) {
  const ref = useRef<HTMLDivElement>(null)
  const inView = useInView(ref, { margin: '-40% 0px -40% 0px' })

  useEffect(() => {
    if (inView) onActive()
  }, [inView, onActive])

  return (
    <div ref={ref} style={{ minHeight: '70vh', display: 'flex', alignItems: 'center' }}>
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: '-10% 0px -10% 0px' }}
        transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
      >
        <div
          style={{
            fontSize: 14,
            fontWeight: 700,
            color: 'var(--coral)',
            letterSpacing: 0.4,
            textTransform: 'uppercase',
            marginBottom: 12,
          }}
        >
          {item.index} {item.kicker}
        </div>
        <h3
          style={{
            fontSize: 'clamp(28px, 4vw, 42px)',
            fontWeight: 700,
            letterSpacing: -1,
            margin: '0 0 18px',
            color: 'var(--ink)',
          }}
        >
          {item.title}
        </h3>
        <p
          style={{
            fontSize: 17,
            lineHeight: 1.7,
            color: 'var(--ink-soft)',
            maxWidth: 480,
            margin: 0,
          }}
        >
          {item.body}
        </p>
      </motion.div>
    </div>
  )
}

export default function Coverage() {
  const [active, setActive] = useState(0)

  return (
    <section id="coverage" style={{ padding: '120px 0' }}>
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
          What's inside
        </p>
        <h2
          style={{
            fontSize: 'clamp(30px, 4.5vw, 48px)',
            fontWeight: 700,
            letterSpacing: -1.2,
            maxWidth: 680,
            marginBottom: 72,
          }}
        >
          Three sections, every single issue
        </h2>

        <div
          className="coverage-grid"
          style={{
            display: 'grid',
            gridTemplateColumns: '1fr 1fr',
            gap: 80,
          }}
        >
          <div>
            {ITEMS.map((item, i) => (
              <CoverageRow key={item.title} item={item} onActive={() => setActive(i)} />
            ))}
          </div>

          <div className="coverage-sticky" style={{ position: 'relative' }}>
            <div style={{ position: 'sticky', top: '18vh', height: '64vh' }}>
              {ITEMS.map((item, i) => (
                <motion.div
                  key={item.title}
                  animate={{ opacity: active === i ? 1 : 0 }}
                  transition={{ duration: 0.5 }}
                  style={{
                    position: 'absolute',
                    inset: 0,
                    borderRadius: 24,
                    background: item.gradient,
                    display: 'flex',
                    alignItems: 'flex-end',
                    padding: 36,
                    overflow: 'hidden',
                  }}
                >
                  <svg
                    width="100%"
                    height="100%"
                    style={{ position: 'absolute', inset: 0, opacity: 0.25 }}
                    viewBox="0 0 400 400"
                    fill="none"
                  >
                    <circle cx="340" cy="60" r="140" stroke="white" strokeWidth="1.5" />
                    <circle cx="40" cy="340" r="100" stroke="white" strokeWidth="1.5" />
                  </svg>
                  <div style={{ color: '#fff', fontSize: 64, fontWeight: 800, opacity: 0.85 }}>
                    {item.index}
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </div>

      <style>{`
        @media (max-width: 900px) {
          .coverage-grid { grid-template-columns: 1fr !important; gap: 40px !important; }
          .coverage-sticky { display: none; }
        }
      `}</style>
    </section>
  )
}
