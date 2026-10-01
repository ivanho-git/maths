import { motion } from 'framer-motion'
import DraggableStack from './DraggableStack'
import { Pop, Sparkle, HeartBubble, Pencil, Globe, Mug } from './Doodles'

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

        {SECTIONS.map((s, sectionIndex) => (
          <div key={s.n} className="service-layout" style={{ display: 'grid', gridTemplateColumns: '42% 58%', gap: 0, minHeight: 760, alignItems: 'start', marginBottom: 110 }}>
            <div className="service-visual" style={{ position: 'relative', minHeight: 650, order: sectionIndex === 1 ? 2 : 0 }}>
              <div className="serif service-number" style={{ fontSize: 'clamp(90px, 15vw, 200px)', lineHeight: 1, textAlign: 'center' }}>{s.n}</div>
              <div style={{ position: 'absolute', top: 170, left: sectionIndex === 1 ? 20 : -48 }} className="stack-placement">
                <DraggableStack items={s.photos.map(p => typeof p === 'string' ? { caption: p } : p)} label={`${s.title.join(' ')} image stack`} />
              </div>
            </div>
            <div className="service-copy" style={{ order: sectionIndex === 1 ? 0 : 2, paddingTop: 24, position: 'relative' }}>
              <Pop style={{ right: '4%', top: 0 }} delay={0.2}>{[<Sparkle size={48} key="a" />, <HeartBubble size={86} key="b" />, <Pencil size={80} key="c" />][sectionIndex]}</Pop>
              <Pop style={{ right: '16%', bottom: 10 }} delay={0.45}>{[<Globe size={64} key="a" />, <Sparkle size={34} key="b" />, <Mug size={70} key="c" />][sectionIndex]}</Pop>
                <div style={{ fontSize: 12, marginBottom: 24, textTransform: 'uppercase' }}>{s.kicker}</div>
                <h2 className="serif" style={{ fontSize: 'clamp(48px, 8vw, 126px)', margin: '0 0 54px' }}>
                  {s.title.map((t, i) => (
                    <motion.span
                      key={t}
                      initial={{ opacity: 0, y: 40 }}
                      whileInView={{ opacity: 1, y: 0 }}
                      viewport={{ once: true }}
                      transition={{ duration: 0.8, delay: i * 0.1, ease: [0.22, 1, 0.36, 1] }}
                      style={{ display: 'block', paddingLeft: i === 1 ? '0.3em' : 0 }}
                    >
                      {t}
                    </motion.span>
                  ))}
                </h2>
                <div style={{ maxWidth: 520, fontSize: 16, lineHeight: 1.6 }}>
                  {s.body.map((p, i) => (
                    <p key={i} style={{ margin: '0 0 28px' }}>{p}</p>
                  ))}
                </div>
                <a href="#subscribe" className="pill" style={{ marginTop: 40 }}>
                  {s.link} <span aria-hidden>→</span>
                </a>
            </div>
          </div>
        ))}
      </div>
      <style>{`@media (max-width: 800px){ .service-layout { display: flex !important; flex-direction: column; min-height: 0 !important; margin-bottom: 90px !important; } .service-copy, .service-visual { width: 100%; order: 0 !important; } .service-visual { min-height: 460px !important; order: 1 !important; } .stack-placement { top: 90px !important; left: 8px !important; } .service-number { text-align: left !important; } .service-copy h2 { font-size: clamp(46px, 11vw, 72px) !important; } }`}</style>
    </section>
  )
}
