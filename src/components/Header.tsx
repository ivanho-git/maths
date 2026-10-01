import { useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'

const LINKS = [
  { href: '/#coverage', label: 'Inside the issue' },
  { href: '/articles', label: 'All articles' },
  { href: '/#method', label: 'Our method' },
  { href: '#subscribe', label: 'Subscribe' },
]

export function Logo({ size = 34 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 40 40" fill="none" aria-label="180 Degrees Consulting">
      <path d="M20 4a16 16 0 1 1-16 16" stroke="var(--red)" strokeWidth="5" strokeLinecap="round" />
      <path d="M4 10v10h10" stroke="var(--red)" strokeWidth="5" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  )
}

export default function Header() {
  const [open, setOpen] = useState(false)

  return (
    <>
      <header style={{ position: 'fixed', top: 0, left: 0, right: 0, zIndex: 60, background: 'var(--cream)' }}>
        <div className="wrap">
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: '1fr auto 1fr',
              alignItems: 'center',
              height: 88,
              borderBottom: '1px solid var(--red)',
            }}
          >
            <a href="/" aria-label="Home" style={{ display: 'flex' }}>
              <Logo />
            </a>
            <span className="caps header-label" style={{ fontSize: 11 }}>The 180° Newsletter</span>
            <div className="header-actions" style={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'center', gap: 28 }}>
              <span
                style={{
                  border: '1px solid var(--red)',
                  borderRadius: 999,
                  padding: '6px 14px',
                  fontSize: 14,
                  fontWeight: 600,
                }}
              >
                EN
              </span>
              <button
                type="button"
                aria-label="Open menu"
                onClick={() => setOpen(true)}
                style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 0, display: 'flex' }}
              >
                <svg width="22" height="18" viewBox="0 0 22 18">
                  <path d="M0 1h22M0 9h22M0 17h22" stroke="var(--red)" strokeWidth="2" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </header>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ clipPath: 'inset(0 0 100% 0)' }}
            animate={{ clipPath: 'inset(0 0 0% 0)' }}
            exit={{ clipPath: 'inset(0 0 100% 0)' }}
            transition={{ duration: 0.6, ease: [0.76, 0, 0.24, 1] }}
            style={{ position: 'fixed', inset: 0, zIndex: 70, background: 'var(--red)', color: 'var(--cream)' }}
          >
            <div className="wrap" style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <div style={{ display: 'flex', justifyContent: 'flex-end', height: 88, alignItems: 'center' }}>
                <button
                  type="button"
                  aria-label="Close menu"
                  onClick={() => setOpen(false)}
                  style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--cream)', fontSize: 34 }}
                >
                  ×
                </button>
              </div>
              <nav style={{ display: 'flex', flexDirection: 'column', gap: 12, marginTop: '6vh' }}>
                {LINKS.map((l, i) => (
                  <motion.a
                    key={l.href}
                    href={l.href}
                    onClick={() => setOpen(false)}
                    initial={{ y: 60, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ delay: 0.25 + i * 0.07, duration: 0.6 }}
                    className="serif"
                    style={{ color: 'var(--cream)', textDecoration: 'none', fontSize: 'clamp(44px, 8vw, 104px)' }}
                  >
                    {l.label}
                  </motion.a>
                ))}
              </nav>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
      <style>{`@media (max-width: 600px) { .header-label { font-size: 8px !important; letter-spacing: .12em !important; white-space: nowrap; } .header-actions { gap: 12px !important; } }`}</style>
    </>
  )
}
