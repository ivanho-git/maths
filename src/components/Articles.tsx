import { useMemo, useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'

type Article = {
  title: string
  category: string
  tone: 'red' | 'ink' | 'pink' | 'outline' | 'photo'
  image?: string
  tall?: boolean
}

const CATEGORIES = ['Impact Stories', 'Chapter News', 'Toolkits', 'Interviews', 'Events', 'Opinion']

// Placeholder articles — replace titles, images and links with real issues.
const ARTICLES: Article[] = [
  { title: 'How Adigo rethought its growth plan with a student team', category: 'Impact Stories', tone: 'photo', image: '/images/adigo.png', tall: true },
  { title: 'Turning plastic waste into a food currency', category: 'Impact Stories', tone: 'red' },
  { title: 'Five interview questions every first-time consultant should ask', category: 'Toolkits', tone: 'pink' },
  { title: 'Launching a chapter from scratch: lessons from year one', category: 'Chapter News', tone: 'ink', tall: true },
  { title: 'What JOY learned about going to market on a tight budget', category: 'Interviews', tone: 'photo', image: '/images/joy-superapps.png' },
  { title: 'Our one-page scoping canvas, free to download', category: 'Toolkits', tone: 'outline' },
  { title: 'Recap: the regional leadership summit', category: 'Events', tone: 'red', tall: true },
  { title: 'Why pro bono work should still be held to a professional standard', category: 'Opinion', tone: 'pink' },
  { title: 'Buy Food with Plastic: from pilot to programme', category: 'Impact Stories', tone: 'photo', image: '/images/buy-food-with-plastic.png' },
  { title: 'Three chapters, one cross-border project', category: 'Chapter News', tone: 'ink' },
]

const TONES = {
  red: { background: 'var(--red)', color: 'var(--cream)', border: 'var(--red)' },
  ink: { background: '#2b1d1f', color: 'var(--cream)', border: '#2b1d1f' },
  pink: { background: '#ffc9cd', color: '#2b1d1f', border: '#ffc9cd' },
  outline: { background: 'transparent', color: 'var(--red)', border: 'var(--red)' },
  photo: { background: '#2b1d1f', color: 'var(--cream)', border: '#2b1d1f' },
}

function Card({ article, index }: { article: Article; index: number }) {
  const t = TONES[article.tone]
  return (
    <motion.a
      layout
      href="#"
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 20 }}
      transition={{ duration: 0.5, delay: (index % 4) * 0.05 }}
      className="article-card"
      style={{
        position: 'relative',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        minHeight: article.tall ? 620 : 420,
        padding: article.tone === 'photo' ? 10 : 26,
        borderRadius: 14,
        border: `1px solid ${t.border}`,
        background: t.background,
        color: t.color,
        textDecoration: 'none',
        overflow: 'hidden',
        breakInside: 'avoid',
        marginBottom: 24,
      }}
    >
      {article.tone === 'photo' ? (
        <>
          <div style={{ position: 'relative', flex: 1, borderRadius: 10, overflow: 'hidden', background: '#fff' }}>
            <img src={article.image} alt="" style={{ width: '100%', height: '100%', objectFit: 'contain', padding: '12%', position: 'absolute', inset: 0 }} />
            <span className="article-pill" style={{ position: 'absolute', top: 20, left: 20, color: '#2b1d1f', borderColor: '#2b1d1f' }}>{article.category}</span>
          </div>
          <div style={{ padding: '22px 16px 14px' }}>
            <h2 className="article-title" style={{ fontSize: 'clamp(30px, 3vw, 44px)' }}>{article.title}</h2>
            <span className="article-more">Read more →</span>
          </div>
        </>
      ) : (
        <>
          <span className="article-pill" style={{ color: t.color, borderColor: t.color }}>{article.category}</span>
          <div>
            <h2 className="article-title" style={{ fontSize: article.tall ? 'clamp(48px, 5.4vw, 86px)' : 'clamp(38px, 4vw, 64px)' }}>{article.title}</h2>
            <span className="article-more">Read more →</span>
          </div>
        </>
      )}
    </motion.a>
  )
}

export default function Articles() {
  const [open, setOpen] = useState(false)
  const [selected, setSelected] = useState<string[]>([])

  const visible = useMemo(
    () => (selected.length ? ARTICLES.filter(a => selected.includes(a.category)) : ARTICLES),
    [selected],
  )

  const toggle = (c: string) => setSelected(s => (s.includes(c) ? s.filter(x => x !== c) : [...s, c]))

  return (
    <main style={{ paddingTop: 120, paddingBottom: 60 }}>
      <div className="wrap">
        <div style={{ display: 'flex', alignItems: 'flex-end', justifyContent: 'space-between', gap: 24, flexWrap: 'wrap', marginBottom: 32 }}>
          <h1 className="serif" style={{ fontSize: 'clamp(56px, 9vw, 140px)', margin: 0 }}>All articles</h1>

          <div style={{ position: 'relative' }}>
            <button type="button" className="pill" onClick={() => setOpen(o => !o)} aria-expanded={open} style={{ position: 'relative', background: 'var(--cream)' }}>
              <svg width="16" height="12" viewBox="0 0 16 12" aria-hidden><path d="M0 1h16M3 6h10M6 11h4" stroke="currentColor" strokeWidth="1.6" /></svg>
              Filter categories
              <span style={{ position: 'absolute', top: -8, right: -8, minWidth: 22, height: 22, borderRadius: 11, background: 'var(--red)', color: 'var(--cream)', fontSize: 11, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '0 6px' }}>
                {visible.length}
              </span>
            </button>

            <AnimatePresence>
              {open && (
                <motion.div
                  initial={{ opacity: 0, y: -8 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -8 }}
                  style={{ position: 'absolute', right: 0, top: 'calc(100% + 10px)', zIndex: 20, width: 280, padding: 20, border: '1px solid var(--red)', borderRadius: 14, background: 'var(--cream)', boxShadow: '6px 6px 0 rgba(255,69,82,0.25)' }}
                >
                  {CATEGORIES.map(c => (
                    <label key={c} style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '7px 0', fontSize: 15, cursor: 'pointer' }}>
                      <input type="checkbox" checked={selected.includes(c)} onChange={() => toggle(c)} style={{ accentColor: 'var(--red)', width: 16, height: 16 }} />
                      {c}
                    </label>
                  ))}
                  <button type="button" onClick={() => setSelected([])} disabled={!selected.length} style={{ marginTop: 12, background: 'none', border: 'none', color: 'var(--red)', textDecoration: 'underline', cursor: 'pointer', padding: 0, opacity: selected.length ? 1 : 0.4 }}>
                    Clear filters
                  </button>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>

        <div className="article-grid">
          <AnimatePresence mode="popLayout">
            {visible.map((a, i) => <Card key={a.title} article={a} index={i} />)}
          </AnimatePresence>
        </div>

        {!visible.length && <p style={{ fontSize: 18 }}>No articles in this category yet.</p>}
      </div>

      <style>{`
        .article-grid { columns: 2; column-gap: 24px; }
        .article-pill { align-self: flex-start; display: inline-block; border: 1px solid; border-radius: 999px; padding: 8px 16px; font-size: 12px; }
        .article-title { font-family: 'Anton', 'Impact', sans-serif; font-weight: 400; line-height: 1; letter-spacing: -0.01em; margin: 0; }
        .article-more { display: inline-block; margin-top: 18px; font-size: 13px; text-transform: uppercase; letter-spacing: 0.15em; opacity: 0; transition: opacity .3s; }
        .article-card:hover .article-more, .article-card:focus-visible .article-more { opacity: 1; }
        .article-card { transition: box-shadow .3s; }
        .article-card:hover { box-shadow: 8px 8px 0 rgba(43,29,31,0.18); }
        @media (max-width: 800px) { .article-grid { columns: 1; } .article-card { min-height: 340px !important; } .article-more { opacity: 1; } }
      `}</style>
    </main>
  )
}
