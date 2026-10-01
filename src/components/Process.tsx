import { motion } from 'framer-motion'

const STEPS = [
  {
    word: 'Listen',
    body: (
      <>
        <strong>Every issue starts with the network.</strong> We collect
        submissions from chapters, alumni and client organisations, and we ask
        what people actually want to read more of. Nothing gets written until
        we know who it is for.
      </>
    ),
  },
  {
    word: 'Edit',
    body: (
      <>
        A small volunteer editorial team turns raw updates into short,
        readable pieces. We cut ruthlessly, check every figure with the team
        that produced it, and make sure each issue holds{' '}
        <strong>one story, one spotlight and one tool</strong>.
      </>
    ),
  },
  {
    word: 'Send',
    body: (
      <>
        On the first Thursday of the month the issue goes out — designed to be
        read on a phone in under five minutes. Replies land straight in our
        inbox, and the best ones shape what we <strong>listen</strong> for
        next time.
      </>
    ),
  },
]

export default function Process() {
  return (
    <section id="method" style={{ padding: '40px 0 120px' }}>
      <div className="wrap">
        <div className="caps" style={{ borderTop: '1px solid var(--red)', paddingTop: 22, marginBottom: 100 }}>
          How each issue is made
        </div>

        {STEPS.map((s, i) => (
          <div
            key={s.word}
            className="method-row"
            style={{
              display: 'grid',
              gridTemplateColumns: i % 2 === 0 ? '1.3fr 1fr' : '1fr 1.3fr',
              gap: 60,
              alignItems: 'center',
              marginBottom: 140,
            }}
          >
            <motion.h2
              initial={{ opacity: 0, x: i % 2 === 0 ? -60 : 60 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true, margin: '-15%' }}
              transition={{ duration: 0.9, ease: [0.22, 1, 0.36, 1] }}
              className="serif"
              style={{
                fontSize: 'clamp(72px, 13vw, 200px)',
                margin: 0,
                order: i % 2 === 0 ? 0 : 1,
                fontStyle: i === 1 ? 'italic' : 'normal',
              }}
            >
              {s.word}
              <span style={{ fontSize: '0.5em' }}>{i < 2 ? ',' : '.'}</span>
            </motion.h2>
            <motion.p
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-15%' }}
              transition={{ duration: 0.8, delay: 0.15 }}
              style={{ fontSize: 17, lineHeight: 1.7, margin: 0, maxWidth: 460 }}
            >
              {s.body}
            </motion.p>
          </div>
        ))}
      </div>
      <style>{`@media (max-width: 800px){ .method-row{ grid-template-columns: 1fr !important; } .method-row > *{ order: 0 !important; } }`}</style>
    </section>
  )
}
