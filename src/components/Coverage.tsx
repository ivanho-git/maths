import { motion } from 'framer-motion'
import Photo from './Photo'

const SECTIONS = [
  {
    n: '1.',
    kicker: 'Case studies, results, lessons learned',
    title: ['Impact', 'Stories'],
    body: [
      'Each month we pick one finished engagement and take it apart: what the client was wrestling with, how the student team scoped the problem, and what actually changed once the recommendations landed.',
      <>Expect honest write-ups — including the parts that didn't go to plan — plus the <strong>numbers</strong> and <strong>client quotes</strong> behind every outcome.</>,
    ],
    link: 'Read the latest story',
    photos: [
      { caption: 'Adigo — strategy support for a growing client.', src: '/images/adigo.png', fit: 'contain' as const },
      { caption: 'Buy Food with Plastic — helping a circular-economy initiative scale.', src: '/images/buy-food-with-plastic.png', fit: 'contain' as const },
      { caption: 'JOY Superapps — go-to-market thinking for a consumer app.', src: '/images/joy-superapps.png', fit: 'contain' as const },
      { caption: 'Concept board: an AI-assisted smart-farming system mapped end to end.', src: '/images/agri-robot-concept.png' },
    ],
  },
  {
    n: '2.',
    kicker: 'Recruitment, events, local partners',
    title: ['Chapter', 'Spotlights'],
    body: [
      'With teams on campuses around the world, something is always happening. We hand the mic to a different chapter every issue so they can share what they are building and who they are building it with.',
      <>From <strong>first-ever cohorts</strong> to chapters celebrating their hundredth project, this is where the network gets to know itself.</>,
    ],
    link: 'Nominate your chapter',
    photos: [
      'Welcome night for a brand-new cohort of consultants.',
      'Regional leadership summit — mostly strategy, partly snacks.',
      'Two chapters, two continents, one shared project call.',
    ],
  },
  {
    n: '3.',
    kicker: 'Templates, frameworks, how-to guides',
    title: ['Tools &', 'Toolkits'],
    body: [
      'The frameworks our teams lean on every week, cleaned up and shared openly. Stakeholder maps, interview guides, scoping checklists — ready to copy into your next project.',
      <>Built for <strong>student consultants</strong> and <strong>nonprofit leaders</strong> alike, with zero jargon and no paywall.</>,
    ],
    link: 'Browse the toolkit',
    photos: [
      'The one-page scoping canvas every new team starts with.',
      'Sticky notes: still undefeated as a prioritisation tool.',
      'Interview prep before a round of beneficiary conversations.',
    ],
  },
]

export default function Coverage() {
  return (
    <section id="coverage" style={{ paddingBottom: 80 }}>
      <div className="wrap">
        <div className="caps" style={{ borderTop: '1px solid var(--red)', paddingTop: 22, marginBottom: 80 }}>
          What's inside?
        </div>

        {SECTIONS.map((s) => (
          <div key={s.n} style={{ marginBottom: 160 }}>
            <div className="svc-grid" style={{ display: 'grid', gridTemplateColumns: '140px 1fr', gap: 24 }}>
              <div className="serif" style={{ fontSize: 'clamp(40px, 6vw, 84px)' }}>{s.n}</div>
              <div>
                <div style={{ fontSize: 14, marginBottom: 22 }}>{s.kicker}</div>
                <h2 className="serif" style={{ fontSize: 'clamp(48px, 7vw, 96px)', margin: '0 0 56px' }}>
                  {s.title.map((t, i) => (
                    <motion.span
                      key={t}
                      initial={{ opacity: 0, y: 40 }}
                      whileInView={{ opacity: 1, y: 0 }}
                      viewport={{ once: true }}
                      transition={{ duration: 0.8, delay: i * 0.1, ease: [0.22, 1, 0.36, 1] }}
                      style={{ display: 'block', paddingLeft: i === 1 ? '1.2em' : 0 }}
                    >
                      {t}
                    </motion.span>
                  ))}
                </h2>
                <div
                  style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
                    gap: 40,
                    fontSize: 16,
                    lineHeight: 1.65,
                  }}
                >
                  {s.body.map((p, i) => (
                    <p key={i} style={{ margin: 0 }}>{p}</p>
                  ))}
                </div>
                <a href="#subscribe" className="pill" style={{ marginTop: 40 }}>
                  {s.link} <span aria-hidden>→</span>
                </a>
              </div>
            </div>

            <div
              className="no-scrollbar"
              style={{
                display: 'grid',
                gridAutoFlow: 'column',
                gridAutoColumns: 'minmax(300px, 40%)',
                gap: 32,
                overflowX: 'auto',
                marginTop: 90,
                scrollSnapType: 'x mandatory',
              }}
            >
              {s.photos.map((p, i) => {
                const c = typeof p === 'string' ? { caption: p } : p
                return (
                <div key={c.caption} style={{ scrollSnapAlign: 'start' }}>
                  <Photo caption={c.caption} src={'src' in c ? c.src : undefined} fit={'fit' in c ? c.fit : 'cover'} index={i} />
                </div>
                )
              })}
            </div>
          </div>
        ))}
      </div>
      <style>{`@media (max-width: 800px){ .svc-grid{ grid-template-columns: 1fr !important; } }`}</style>
    </section>
  )
}
