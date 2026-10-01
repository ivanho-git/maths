import { useEffect, useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'

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
    <section id="top" style={{ paddingTop: 88 }}>
      <div className="wrap">
        <h1 style={{ position: 'absolute', width: 1, height: 1, overflow: 'hidden', clip: 'rect(0 0 0 0)' }}>
          The 180 Degrees Consulting Newsletter
        </h1>
        <div style={{ minHeight: '92vh', display: 'flex', alignItems: 'center', padding: '48px 0' }}>
          <AnimatePresence mode="wait">
            <div key={i} style={{ width: '100%' }}>
              {SLIDES[i].map((line, li) => (
                <div
                  key={line.word}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: 28,
                    flexDirection: line.align === 'left' ? 'row-reverse' : 'row',
                    justifyContent: line.align === 'left' ? 'flex-end' : 'flex-start',
                  }}
                >
                  <span className="serif" style={{ fontSize: 'clamp(56px, 11.5vw, 170px)' }}>
                    <Letters text={line.word} delay={li * 0.08} />
                  </span>
                  {line.note && (
                    <motion.span
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      exit={{ opacity: 0 }}
                      transition={{ delay: 0.5 + li * 0.1 }}
                      style={{ fontSize: 11, textTransform: 'uppercase', lineHeight: 1.4, letterSpacing: 0.4 }}
                    >
                      {line.note[0]}
                      <br />
                      <strong>{line.note[1]}</strong>
                    </motion.span>
                  )}
                </div>
              ))}
            </div>
          </AnimatePresence>
        </div>

        <div className="hero-intro" style={{ display: 'flex', justifyContent: 'flex-end', padding: '80px 0 200px' }}>
          <div style={{ width: '100%', maxWidth: 560, fontSize: 'clamp(20px, 2.2vw, 30px)', lineHeight: 1.35 }}>
          <p style={{ margin: '0 0 52px' }}>
            <strong>180 Degrees Consulting</strong> is the world's largest
            student-run consultancy, pairing university teams with nonprofits
            and social enterprises — at no cost to them.
          </p>
          <p style={{ margin: 0 }}>
            This newsletter is our monthly dispatch: the projects that
            shipped, the chapters making noise, and the{' '}
            <strong>tools you can steal</strong> for your own work.
          </p>
          </div>
        </div>
      </div>
    </section>
  )
}
