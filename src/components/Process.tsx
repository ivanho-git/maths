import { motion } from 'framer-motion'

const STEPS = [
  {
    num: '01',
    title: 'Discover',
    body: 'We gather the month\'s submissions from chapters worldwide — project wins, lessons learned, and the questions volunteers are asking.',
  },
  {
    num: '02',
    title: 'Curate',
    body: 'Our editorial team shortlists the stories and resources most useful to nonprofit leaders and student consultants alike.',
  },
  {
    num: '03',
    title: 'Deliver',
    body: 'One concise, well-designed email lands in your inbox — no fluff, just the updates and tools worth your five minutes.',
  },
]

export default function Process() {
  return (
    <section
      id="process"
      style={{ padding: '120px 0', background: 'var(--navy)', color: '#fff' }}
    >
      <div className="container-x">
        <p
          style={{
            fontSize: 14,
            fontWeight: 700,
            color: '#ff9a7f',
            letterSpacing: 0.4,
            textTransform: 'uppercase',
            marginBottom: 16,
          }}
        >
          How it comes together
        </p>
        <h2
          style={{
            fontSize: 'clamp(30px, 4.5vw, 48px)',
            fontWeight: 700,
            letterSpacing: -1.2,
            maxWidth: 680,
            marginBottom: 64,
            color: '#fff',
          }}
        >
          Discover, curate, deliver
        </h2>

        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
            gap: 48,
          }}
        >
          {STEPS.map((step, i) => (
            <motion.div
              key={step.num}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-10%' }}
              transition={{ duration: 0.6, delay: i * 0.12, ease: [0.22, 1, 0.36, 1] }}
              style={{
                borderTop: '1px solid rgba(255,255,255,0.15)',
                paddingTop: 28,
              }}
            >
              <div
                style={{
                  fontSize: 15,
                  fontWeight: 700,
                  color: '#ff5a36',
                  marginBottom: 18,
                }}
              >
                {step.num}
              </div>
              <h3 style={{ fontSize: 24, fontWeight: 700, margin: '0 0 14px', color: '#fff' }}>
                {step.title}
              </h3>
              <p style={{ fontSize: 16, lineHeight: 1.7, color: 'rgba(255,255,255,0.65)', margin: 0 }}>
                {step.body}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
