import { useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'

const LINKS = [
  { href: '/', label: 'Home' },
  { href: '/articles', label: 'All articles' },
  { href: '/#method', label: 'How it works' },
  { href: '#subscribe', label: 'Subscribe' },
]

export function Logo({ size = 34 }: { size?: number; color?: string }) {
  return <img src="/images/180dc-mark.png" width={size} height={size} alt="180 Degrees Consulting" style={{ display: 'block', objectFit: 'contain' }} />
}

export default function Header() {
  const [open, setOpen] = useState(false)

  return (
    <>
      <nav className="pill-nav">
        <a href="#subscribe" className="pill-nav-side">Subscribe</a>
        <a href="/" className="pill-nav-logo" aria-label="Home">
          <Logo size={24} /> <span>180° Newsletter</span>
        </a>
        <button type="button" className="pill-nav-side" onClick={() => setOpen(true)} aria-label="Open menu">Menu</button>
      </nav>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ clipPath: 'inset(0 0 100% 0)' }}
            animate={{ clipPath: 'inset(0 0 0% 0)' }}
            exit={{ clipPath: 'inset(0 0 100% 0)' }}
            transition={{ duration: 0.6, ease: [0.76, 0, 0.24, 1] }}
            style={{ position: 'fixed', inset: 0, zIndex: 70, background: 'var(--green)', color: '#fff' }}
          >
            <div className="wrap" style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <div style={{ display: 'flex', justifyContent: 'flex-end', height: 120, alignItems: 'center' }}>
                <button type="button" aria-label="Close menu" onClick={() => setOpen(false)} className="pill" style={{ padding: '10px 18px' }}>
                  Close ×
                </button>
              </div>
              <nav style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                {LINKS.map((l, i) => (
                  <motion.a
                    key={l.href}
                    href={l.href}
                    onClick={() => setOpen(false)}
                    initial={{ y: 60, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ delay: 0.25 + i * 0.07, duration: 0.6 }}
                    className="serif"
                    style={{ color: '#fff', textDecoration: 'none', fontSize: 'clamp(52px, 9vw, 120px)' }}
                  >
                    {l.label}
                  </motion.a>
                ))}
              </nav>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <style>{`
        .pill-nav { position: fixed; top: 28px; left: 50%; transform: translateX(-50%); z-index: 60; display: grid; grid-template-columns: auto 1fr auto; align-items: center; width: min(440px, calc(100vw - 32px)); height: 50px; background: #fff; border: 1.5px solid var(--ink); border-radius: 999px; box-shadow: var(--shadow); }
        .pill-nav-side { padding: 0 18px; font-family: var(--serif); font-size: 15px; text-transform: uppercase; color: var(--ink); text-decoration: none; height: 26px; display: flex; align-items: center; background: none; border: none; cursor: pointer; }
        .pill-nav-side:first-child { border-right: 2px solid var(--ink); }
        .pill-nav-side:last-child { border-left: 2px solid var(--ink); }
        .pill-nav-logo { display: flex; align-items: center; justify-content: center; gap: 8px; color: var(--ink); text-decoration: none; font-family: var(--serif); font-size: 18px; white-space: nowrap; }
        @media (max-width: 420px) { .pill-nav-logo span { display: none; } }
      `}</style>
    </>
  )
}
