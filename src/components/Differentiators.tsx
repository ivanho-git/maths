import { motion } from 'framer-motion'
import Photo from './Photo'

const POINTS = [
  {
    title: 'Global',
    body: 'Stories come from every corner of the network, so you hear how the same nonprofit challenge looks in Sydney, São Paulo and Seoul.',
  },
  {
    title: 'Practical',
    body: 'Every issue includes at least one template or framework you can put to work the same week — no theory without a takeaway.',
  },
  {
    title: 'Honest',
    body: 'We publish what worked and what did not. Failed hypotheses teach as much as successful ones, so we keep both in.',
  },
  {
    title: 'Free',
    body: 'Our consulting is pro bono and so is the newsletter. No paywall, no premium tier, no selling your email address.',
  },
]

const GALLERY = [
  'Consultants and client staff working through a problem tree together.',
  'Late-night slide polishing before a board presentation.',
  'Chapter presidents comparing notes at the annual meetup.',
  'A field visit to see the programme the team was advising on.',
  'Celebrating the end of a project cycle.',
  'New members on their first training weekend.',
]

export default function Differentiators() {
  return (
    <section id="why" style={{ padding: '40px 0 120px' }}>
      <div className="wrap">
        <div className="caps" style={{ borderTop: '1px solid var(--red)', paddingTop: 22, marginBottom: 80 }}>
          Why read us
        </div>

        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
            gap: '64px 80px',
            marginBottom: 120,
          }}
        >
          {POINTS.map((p, i) => (
            <motion.div
              key={p.title}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.7, delay: (i % 2) * 0.12 }}
            >
              <h2 className="serif" style={{ fontSize: 'clamp(44px, 5.5vw, 76px)', margin: '0 0 20px' }}>{p.title}</h2>
              <p style={{ fontSize: 16, lineHeight: 1.65, margin: 0, maxWidth: 440 }}>{p.body}</p>
            </motion.div>
          ))}
        </div>

        <div className="gallery" style={{ columnCount: 3, columnGap: 32 }}>
          {GALLERY.map((c, i) => (
            <div key={c} style={{ breakInside: 'avoid', marginBottom: 40 }}>
              <Photo caption={c} index={i} ratio={i % 3 === 1 ? '3/4' : i % 2 ? '1/1' : '4/3'} />
            </div>
          ))}
        </div>
      </div>
      <style>{`@media (max-width: 900px){ .gallery{ column-count: 2 !important; } } @media (max-width: 560px){ .gallery{ column-count: 1 !important; } }`}</style>
    </section>
  )
}
