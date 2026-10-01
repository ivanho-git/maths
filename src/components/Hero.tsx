import { useEffect, useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import { Megaphone, PaperPlane, Sparkle, HeartBubble, Pencil, Mug, Globe, BrushStroke } from './Doodles'
import { Strider } from './Figures'

type Line = { word: string; note?: string[]; align?: 'left' | 'right' }

const SLIDES: Line[][] = [
  [
    { word: 'Change', note: ['Chapters', '180+'] },
    { word: 'Starts', note: ['Across', '38 countries'], align: 'left' },
    { word: 'On campus', note: ['Since', '2007'] },
  ],
  [
    { word: 'Students' },
    { word: 'Solving', note: ['Pro bono', 'for every client'] },
    { word: 'Real' },
    { word: 'Problems' },
  ],
  [
    { word: 'Turn it' , note: ['One issue', 'a month'] },
    { word: 'Right', note: ['Five minutes', 'to read it'], align: 'left' },
    { word: 'Around', note: ['Zero spam', 'we promise'] },
  ],
]

function Letters({ text, delay }: { text: string; delay: number }) {
  return (
    <span style={{ display: 'inline-flex', overflow: 'hidden', paddingBottom: '0.06em' }}>
      {text.split('').map((ch, i) => (
        <motion.span
          key={i}
          initial={{ y: '105%' }}
          animate={{ y: 0 }}
          exit={{ y: '-105%' }}
          transition={{ duration: 0.7, delay: delay + i * 0.025, ease: [0.76, 0, 0.24, 1] }}
          style={{ display: 'inline-block', whiteSpace: 'pre' }}
        >
          {ch}
        </motion.span>
      ))}
    </span>
  )
}

export default function Hero() {
  const [i, setI] = useState(0)

  useEffect(() => {
    const t = setInterval(() => setI((v) => (v + 1) % SLIDES.length), 4200)
    return () => clearInterval(t)
  }, [])

  return (
    <section id="top" style={{ padding: '14px 14px 0' }}>
      <h1 style={{ position: 'absolute', width: 1, height: 1, overflow: 'hidden', clip: 'rect(0 0 0 0)' }}>
        The 180 Degrees Consulting Newsletter
      </h1>
      <div className="hero-band">
        <Megaphone size={120} style={{ position: 'absolute', left: '6%', top: '22%', transform: 'rotate(-14deg)' }} />
        <PaperPlane size={110} style={{ position: 'absolute', right: '8%', top: '18%' }} />
        <HeartBubble size={86} style={{ position: 'absolute', left: '14%', top: '56%' }} />
        <Sparkle size={40} style={{ position: 'absolute', left: '28%', top: '16%' }} />
        <Sparkle size={30} style={{ position: 'absolute', right: '24%', top: '62%' }} />
        <Pencil size={84} style={{ position: 'absolute', right: '12%', bottom: '18%' }} />
        <Mug size={74} style={{ position: 'absolute', left: '9%', bottom: '10%' }} />
        <Globe size={70} style={{ position: 'absolute', right: '30%', top: '9%' }} />
        <div style={{ position: 'relative', zIndex: 2, minHeight: 470, display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center' }}>
          <AnimatePresence mode="wait">
            <div key={i}>
              {SLIDES[i].map((line, li) => (
                <div key={line.word} style={{ lineHeight: 0.9, margin: '6px 0' }}>
                  <span className="serif" style={{ fontSize: 'clamp(54px, 9.5vw, 150px)', color: li === 1 ? '#fff' : 'var(--ink)', padding: li === 1 ? '0.04em 0.16em' : 0, display: 'inline-block', position: 'relative', zIndex: 0 }}>
                    {li === 1 && <BrushStroke />}
                    <Letters text={line.word} delay={li * 0.08} />
                  </span>
                </div>
              ))}
            </div>
          </AnimatePresence>
        </div>
        <Strider size={240} style={{ position: 'relative', zIndex: 3, display: 'block', margin: '-40px auto 0' }} />
        <p className="serif" style={{ fontSize: 22, margin: '18px 0 22px', textAlign: 'center' }}>This newsletter is made for you</p>
        <div style={{ textAlign: 'center', paddingBottom: 56 }}>
          <a href="#subscribe" className="pill" style={{ background: 'var(--green)', color: '#fff' }}>Subscribe for free</a>
        </div>
      </div>

      <div className="wrap" style={{ padding: '110px 0 140px', textAlign: 'center' }}>
        <p className="serif" style={{ fontSize: 'clamp(28px, 3.6vw, 52px)', lineHeight: 1.08, maxWidth: 1000, margin: '0 auto' }}>
          180 Degrees Consulting is the world's largest student-run consultancy, pairing university teams with nonprofits and social enterprises at no cost.
          {' '}<span style={{ color: 'var(--green)' }}>Every month we share the projects that shipped, the chapters making noise and the tools you can borrow.</span>
        </p>
      </div>

      <style>{`
        .hero-band > svg { animation: bob 5s ease-in-out infinite; } .hero-band > svg:nth-of-type(2n) { animation-duration: 6.5s; animation-delay: -2s; }
        .hero-band { position: relative; overflow: hidden; background: var(--lilac); border-radius: 28px; padding-top: 110px; }
        @media (max-width: 800px) { .hero-band svg:not([aria-label]) { transform: scale(.7); } }
      `}</style>
    </section>
  )
}
