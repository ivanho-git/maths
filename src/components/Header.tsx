import { useEffect, useState } from 'react'

const NAV_LINKS = [
  { href: '#coverage', label: 'Newsletter' },
  { href: '#process', label: 'How It Works' },
  { href: '#why', label: 'Why Subscribe' },
  { href: '#chapters', label: 'Chapters' },
]

export default function Header() {
  const [scrolled, setScrolled] = useState(false)
  const [menuOpen, setMenuOpen] = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 24)
    onScroll()
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  return (
    <header
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        zIndex: 50,
        transition: 'background 0.3s ease, box-shadow 0.3s ease',
        background: scrolled ? 'rgba(251,250,248,0.92)' : 'transparent',
        backdropFilter: scrolled ? 'blur(10px)' : 'none',
        boxShadow: scrolled ? '0 1px 0 var(--line)' : 'none',
      }}
    >
      <div
        className="container-x"
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          height: 76,
        }}
      >
        <a
          href="#top"
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 10,
            textDecoration: 'none',
            color: 'var(--ink)',
            fontWeight: 700,
            fontSize: 18,
          }}
        >
          <span
            style={{
              width: 32,
              height: 32,
              borderRadius: '50%',
              background: 'var(--navy)',
              color: '#fff',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: 11,
              fontWeight: 800,
            }}
          >
            180
          </span>
          180° Consulting
          <span style={{ color: 'var(--coral)', fontWeight: 600 }}>
            Newsletter
          </span>
        </a>

        <nav
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 32,
          }}
          className="desktop-nav"
        >
          {NAV_LINKS.map((link) => (
            <a
              key={link.href}
              href={link.href}
              style={{
                color: 'var(--ink-soft)',
                textDecoration: 'none',
                fontSize: 15,
                fontWeight: 500,
              }}
            >
              {link.label}
            </a>
          ))}
          <a
            href="#subscribe"
            style={{
              background: 'var(--coral)',
              color: '#fff',
              padding: '10px 20px',
              borderRadius: 999,
              fontSize: 14,
              fontWeight: 600,
              textDecoration: 'none',
            }}
          >
            Subscribe
          </a>
        </nav>

        <button
          type="button"
          onClick={() => setMenuOpen((v) => !v)}
          className="mobile-nav-toggle"
          aria-label="Toggle menu"
          style={{
            display: 'none',
            background: 'none',
            border: 'none',
            cursor: 'pointer',
            padding: 8,
          }}
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path
              d="M3 6h18M3 12h18M3 18h18"
              stroke="var(--ink)"
              strokeWidth="2"
              strokeLinecap="round"
            />
          </svg>
        </button>
      </div>

      {menuOpen && (
        <div
          className="container-x"
          style={{
            display: 'flex',
            flexDirection: 'column',
            gap: 16,
            paddingBottom: 24,
            background: 'var(--paper)',
          }}
        >
          {NAV_LINKS.map((link) => (
            <a
              key={link.href}
              href={link.href}
              onClick={() => setMenuOpen(false)}
              style={{ color: 'var(--ink)', textDecoration: 'none', fontSize: 16, fontWeight: 500 }}
            >
              {link.label}
            </a>
          ))}
          <a
            href="#subscribe"
            onClick={() => setMenuOpen(false)}
            style={{
              background: 'var(--coral)',
              color: '#fff',
              padding: '12px 20px',
              borderRadius: 999,
              fontSize: 14,
              fontWeight: 600,
              textDecoration: 'none',
              textAlign: 'center',
            }}
          >
            Subscribe
          </a>
        </div>
      )}

      <style>{`
        @media (max-width: 860px) {
          .desktop-nav { display: none !important; }
          .mobile-nav-toggle { display: inline-flex !important; }
        }
      `}</style>
    </header>
  )
}
