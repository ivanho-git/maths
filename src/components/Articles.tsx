import { useMemo, useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'

type Article = { title: string; category: string; tone: 'red' | 'ink' | 'pink'; image?: string; fit?: 'contain' | 'cover' }

const CATEGORIES = ['Impact Stories', 'Chapter News', 'Toolkits', 'Interviews', 'Events', 'Opinion']

// Placeholder articles — replace with real issues.
const ARTICLES: Article[] = [
  { title: 'How Adigo rethought its growth plan with a student team', category: 'Impact Stories', tone: 'red', image: '/images/adigo.png', fit: 'contain' },
  { title: 'Turning plastic waste into a food currency', category: 'Impact Stories', tone: 'ink', image: '/images/buy-food-with-plastic.png', fit: 'contain' },
  { title: 'Five interview questions every first-time consultant should ask', category: 'Toolkits', tone: 'pink' },
  { title: 'Launching a chapter from scratch: lessons from year one', category: 'Chapter News', tone: 'red' },
  { title: 'What JOY learned about going to market on a tight budget', category: 'Interviews', tone: 'pink', image: '/images/joy-superapps.png', fit: 'contain' },
  { title: 'Our one-page scoping canvas, free to download', category: 'Toolkits', tone: 'ink' },
  { title: 'Recap: the regional leadership summit', category: 'Events', tone: 'red' },
  { title: 'Why pro bono work should still be held to a professional standard', category: 'Opinion', tone: 'ink' },
  { title: 'Buy Food with Plastic: from pilot to programme', category: 'Impact Stories', tone: 'pink' },
  { title: 'Three chapters, one cross-border project', category: 'Chapter News', tone: 'red' },
]

const TONE = {
  red: { bg: 'var(--green)', fg: '#fff', frame: '#fff' },
  ink: { bg: 'var(--ink)', fg: '#fff', frame: '#fff' },
  pink: { bg: 'var(--lilac)', fg: '#fff', frame: '#fff' },
}

const SHADOW = 'var(--shadow)'

function Card({ a, i }: { a: Article; i: number }) {
  const t = TONE[a.tone]
  return (
    <motion.li layout initial={{ opacity: 0, y: 40 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, scale: 0.97 }} transition={{ duration: 0.45, delay: (i % 2) * 0.06 }} style={{ listStyle: 'none' }}>
      <a href="#" className="hr-card" style={{ background: t.bg, color: t.fg }}>
        {a.image && (
          <div className="hr-frame" style={{ background: '#fff' }}>
            <img src={a.image} alt="" style={{ objectFit: a.fit ?? 'cover', padding: a.fit === 'contain' ? '14%' : 0 }} />
          </div>
        )}
        <div className="hr-card-top">
          <span className="hr-pill" style={{ borderColor: t.fg, color: t.fg }}>{a.category}</span>
          <span className="hr-arrow" aria-hidden>↗</span>
        </div>
        <h2 className="hr-title">{a.title}</h2>
      </a>
    </motion.li>
  )
}

function Letters({ text }: { text: string }) {
  return (
    <>
      {text.split(' ').map((w, wi) => (
        <span key={wi} style={{ display: 'inline-block', marginRight: '0.25em', whiteSpace: 'nowrap' }}>
          {w.split('').map((c, ci) => (
            <motion.span key={ci} initial={{ y: '0.6em', opacity: 0 }} whileInView={{ y: 0, opacity: 1 }} viewport={{ once: true }} transition={{ delay: (wi * 4 + ci) * 0.02, duration: 0.5 }} style={{ display: 'inline-block' }}>
              {c}
            </motion.span>
          ))}
        </span>
      ))}
    </>
  )
}

export default function Articles() {
  const [open, setOpen] = useState(false)
  const [selected, setSelected] = useState<string[]>([])
  const visible = useMemo(() => (selected.length ? ARTICLES.filter(a => selected.includes(a.category)) : ARTICLES), [selected])
  const toggle = (c: string) => setSelected(s => (s.includes(c) ? s.filter(x => x !== c) : [...s, c]))

  return (
    <div className="hr-page">

      <div className="hr-filter">
        <button type="button" className="hr-filter-btn" onClick={() => setOpen(o => !o)} aria-expanded={open}>
          <svg width="16" height="12" viewBox="0 0 16 12" aria-hidden><path d="M0 1h16M3 6h10M6 11h4" stroke="currentColor" strokeWidth="1.6" /></svg>
          Filter categories
          <span className="hr-badge">{visible.length}</span>
          {open && <span aria-hidden style={{ marginLeft: 6 }}>×</span>}
        </button>
        <AnimatePresence>
          {open && (
            <motion.div className="hr-filter-panel" initial={{ opacity: 0, y: -6 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -6 }}>
              {CATEGORIES.map(c => (
                <label key={c}>
                  <input type="checkbox" checked={selected.includes(c)} onChange={() => toggle(c)} />
                  {c}
                </label>
              ))}
              <button type="button" className="hr-clear" onClick={() => setSelected([])} aria-label="Clear filters">🗑</button>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      <ul className="hr-grid">
        <AnimatePresence mode="popLayout">
          {visible.map((a, i) => <Card key={a.title} a={a} i={i} />)}
        </AnimatePresence>
      </ul>
      {!visible.length && <p style={{ textAlign: 'center' }}>No articles in this category yet.</p>}

      <section className="hr-cta">
        <h2 className="hr-cta-title"><Letters text="Want every story? Get the free monthly issue in your inbox" /></h2>
        <a href="#subscribe" className="hr-cta-btn">Subscribe for free</a>
      </section>

      <style>{`
        .hr-page { background: var(--cream); color: var(--ink); padding: 0 26px 40px; }
        .hr-nav { position: fixed; top: 38px; left: 50%; transform: translateX(-50%); z-index: 60; display: grid; grid-template-columns: auto 1fr auto; align-items: center; width: min(430px, calc(100vw - 40px)); height: 50px; background: #fff; border: 1.5px solid var(--ink); border-radius: 999px; box-shadow: ${SHADOW}; }
        .hr-nav-side { padding: 0 18px; font-family: 'Anton', sans-serif; font-size: 15px; text-transform: uppercase; color: var(--ink); text-decoration: none; height: 26px; display: flex; align-items: center; }
        .hr-nav-side:first-child { border-right: 2px solid var(--ink); } .hr-nav-side:last-child { border-left: 2px solid var(--ink); }
        .hr-nav-logo { display: flex; align-items: center; justify-content: center; gap: 8px; color: var(--ink); text-decoration: none; font-family: 'Anton', sans-serif; font-size: 18px; }
        .hr-filter { position: sticky; top: 110px; z-index: 50; margin-top: 110px; margin-bottom: 16px; width: max-content; }
        .hr-filter-btn { position: relative; display: flex; align-items: center; gap: 12px; padding: 12px 20px; background: #fff; border: 1.5px solid var(--ink); border-radius: 999px; box-shadow: ${SHADOW}; font-family: 'Anton', sans-serif; font-size: 16px; color: var(--ink); cursor: pointer; }
        .hr-badge { position: absolute; top: -9px; right: -9px; min-width: 20px; height: 20px; padding: 0 5px; border-radius: 10px; background: var(--lilac); border: 1px solid var(--ink); font-family: Inter, sans-serif; font-size: 11px; display: flex; align-items: center; justify-content: center; }
        .hr-filter-panel { position: absolute; top: calc(100% + 10px); left: 0; width: 290px; padding: 18px 20px; background: #fff; border: 1.5px solid var(--ink); border-radius: 22px; box-shadow: ${SHADOW}; }
        .hr-filter-panel label { display: flex; gap: 10px; align-items: center; padding: 6px 0; font-size: 15px; cursor: pointer; }
        .hr-filter-panel input { width: 17px; height: 17px; accent-color: var(--red); }
        .hr-clear { margin-top: 8px; background: none; border: none; cursor: pointer; font-size: 18px; padding: 0; }
        .hr-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; padding: 0; margin: 0; }
        .hr-card { position: relative; display: flex; flex-direction: column; justify-content: flex-end; gap: 22px; min-height: 460px; padding: 10px 24px 34px; border-radius: 16px; text-decoration: none; overflow: hidden; height: 100%; }
        .hr-frame { position: relative; flex: 1; min-height: 300px; margin: 0 -14px 4px; border-radius: 12px; overflow: hidden; }
        .hr-frame img { position: absolute; inset: 0; width: 100%; height: 100%; transition: transform .6s; }
        .hr-card:hover .hr-frame img { transform: scale(1.04); }
        .hr-card-top { display: flex; justify-content: space-between; align-items: center; }
        .hr-frame + .hr-card-top { position: absolute; top: 34px; left: 34px; right: 34px; }
        .hr-card:not(:has(.hr-frame)) .hr-card-top { position: absolute; top: 34px; left: 24px; right: 24px; }
        .hr-pill { border: 1px solid; border-radius: 999px; padding: 8px 16px; font-size: 12px; background: transparent; }
        .hr-frame + .hr-card-top .hr-pill { color: var(--ink) !important; border-color: var(--ink) !important; }
        .hr-arrow { width: 44px; height: 44px; border-radius: 50%; background: #fff; color: var(--ink); border: 1.5px solid var(--ink); box-shadow: ${SHADOW}; display: flex; align-items: center; justify-content: center; font-size: 18px; opacity: 0; transition: opacity .25s; }
        .hr-card:hover .hr-arrow, .hr-card:focus-visible .hr-arrow { opacity: 1; }
        .hr-title { font-family: 'Anton', sans-serif; font-weight: 400; font-size: clamp(34px, 4vw, 60px); line-height: 1.02; margin: 0; }
        .hr-cta { text-align: center; padding: 140px 0 60px; }
        .hr-cta-title { font-family: 'Anton', sans-serif; font-weight: 400; text-transform: lowercase; font-size: clamp(56px, 9vw, 150px); line-height: 0.95; max-width: 1200px; margin: 0 auto 40px; color: var(--ink); }
        .hr-cta-btn { display: inline-block; padding: 16px 30px; border-radius: 999px; background: var(--red); color: var(--cream); border: 1.5px solid var(--ink); box-shadow: ${SHADOW}; text-decoration: none; text-transform: uppercase; font-size: 14px; letter-spacing: .05em; }
        @media (max-width: 800px) { .hr-grid { grid-template-columns: 1fr; } .hr-card { min-height: 380px; } .hr-filter { top: 100px; } .hr-nav { top: 20px; } }
      `}</style>
    </div>
  )
}
