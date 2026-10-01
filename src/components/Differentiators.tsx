import { motion } from 'framer-motion'
import Photo from './Photo'
import { Reader, Waver } from './Figures'

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

        <div className="why-tiles">
          {POINTS.map((p, i) => {
            const bg = ['var(--ink)', 'var(--green)', 'var(--green)', 'var(--lilac)'][i]
            return (
              <motion.div
                key={p.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: (i % 2) * 0.1 }}
                className="why-tile"
                style={{ background: bg, marginTop: i % 2 ? 90 : 0 }}
              >
                <h3 className="serif" style={{ fontSize: 'clamp(34px, 3.6vw, 52px)', margin: '0 0 14px', color: '#fff' }}>{p.title}</h3>
                <p style={{ fontSize: 16, lineHeight: 1.6, margin: 0, color: '#fff', maxWidth: 360 }}>{p.body}</p>
              </motion.div>
            )
          })}
          <Reader size={200} style={{ position: 'absolute', left: '38%', bottom: -70 }} />
          <Waver size={170} style={{ position: 'absolute', right: -10, bottom: -60 }} />
        </div>
        <style>{`.why-tiles { position: relative; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 160px; } .why-tile { border-radius: 18px; padding: 30px; min-height: 260px; display: flex; flex-direction: column; justify-content: flex-end; } @media (max-width: 800px) { .why-tiles { grid-template-columns: 1fr; } .why-tile { margin-top: 0 !important; } }`}</style>

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
