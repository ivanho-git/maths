import { motion } from 'framer-motion'

const fadeUp = {
  hidden: { opacity: 0, y: 24 },
  show: (delay = 0) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.7, delay, ease: [0.22, 1, 0.36, 1] },
  }),
}

export default function Hero() {
  return (
    <section
      id="top"
      style={{
        position: 'relative',
        paddingTop: 170,
        paddingBottom: 100,
        overflow: 'hidden',
        background:
          'radial-gradient(circle at 15% 20%, rgba(255,90,54,0.10), transparent 45%), radial-gradient(circle at 85% 0%, rgba(16,25,47,0.06), transparent 40%)',
      }}
    >
      <div className="container-x">
        <motion.p
          initial="hidden"
          animate="show"
          variants={fadeUp}
          custom={0}
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: 8,
            padding: '6px 14px',
            borderRadius: 999,
            border: '1px solid var(--line)',
            fontSize: 13,
            fontWeight: 600,
            letterSpacing: 0.4,
            textTransform: 'uppercase',
            color: 'var(--coral)',
            background: 'var(--coral-soft)',
            marginBottom: 28,
          }}
        >
          The 180° Consulting Newsletter
        </motion.p>

        <motion.h1
          initial="hidden"
          animate="show"
          variants={fadeUp}
          custom={0.1}
          style={{
            fontSize: 'clamp(40px, 6vw, 76px)',
            lineHeight: 1.04,
            letterSpacing: -1.5,
            fontWeight: 700,
            margin: 0,
            maxWidth: 820,
            color: 'var(--ink)',
          }}
        >
          We turn student insight into
          <span style={{ color: 'var(--coral)' }}> nonprofit impact</span>
        </motion.h1>

        <motion.p
          initial="hidden"
          animate="show"
          variants={fadeUp}
          custom={0.22}
          style={{
            fontSize: 19,
            lineHeight: 1.6,
            color: 'var(--ink-soft)',
            maxWidth: 560,
            marginTop: 28,
          }}
        >
          Every month we round up project case studies, chapter news and free
          consulting toolkits from the world's largest student-run
          consultancy — delivered straight to your inbox.
        </motion.p>

        <motion.div
          initial="hidden"
          animate="show"
          variants={fadeUp}
          custom={0.32}
          style={{ display: 'flex', gap: 14, marginTop: 36, flexWrap: 'wrap' }}
        >
          <a
            href="#subscribe"
            style={{
              background: 'var(--navy)',
              color: '#fff',
              padding: '14px 28px',
              borderRadius: 999,
              fontWeight: 600,
              fontSize: 15,
              textDecoration: 'none',
            }}
          >
            Subscribe for free
          </a>
          <a
            href="#coverage"
            style={{
              border: '1px solid var(--line)',
              color: 'var(--ink)',
              padding: '14px 28px',
              borderRadius: 999,
              fontWeight: 600,
              fontSize: 15,
              textDecoration: 'none',
            }}
          >
            See what's inside
          </a>
        </motion.div>

        <motion.div
          initial="hidden"
          animate="show"
          variants={fadeUp}
          custom={0.44}
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))',
            gap: 28,
            marginTop: 72,
            maxWidth: 760,
            borderTop: '1px solid var(--line)',
            paddingTop: 32,
          }}
        >
          {[
            { value: '38', label: 'Countries with active chapters' },
            { value: '14K+', label: 'Students volunteered since 2007' },
            { value: '100%', label: 'Free consulting for nonprofits' },
          ].map((stat) => (
            <div key={stat.label}>
              <div
                style={{
                  fontSize: 34,
                  fontWeight: 700,
                  color: 'var(--navy)',
                  letterSpacing: -1,
                }}
              >
                {stat.value}
              </div>
              <div style={{ fontSize: 14, color: 'var(--ink-soft)', marginTop: 4 }}>
                {stat.label}
              </div>
            </div>
          ))}
        </motion.div>
      </div>
    </section>
  )
}
