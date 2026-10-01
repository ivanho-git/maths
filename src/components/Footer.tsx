import { useState } from 'react'

export default function Footer() {
  const [email, setEmail] = useState('')
  const [submitted, setSubmitted] = useState(false)

  return (
    <footer id="subscribe" style={{ background: '#fff', borderTop: '1px solid var(--line)' }}>
      <div className="container-x" style={{ padding: '100px 0 48px' }}>
        <div
          style={{
            textAlign: 'center',
            maxWidth: 560,
            margin: '0 auto 64px',
          }}
        >
          <h2
            style={{
              fontSize: 'clamp(28px, 4vw, 42px)',
              fontWeight: 700,
              letterSpacing: -1,
              margin: '0 0 16px',
            }}
          >
            Get the next issue
          </h2>
          <p style={{ fontSize: 16, color: 'var(--ink-soft)', margin: '0 0 32px' }}>
            One email a month. Impact stories, chapter news, and free
            consulting resources. Unsubscribe anytime.
          </p>

          {submitted ? (
            <div
              style={{
                padding: '16px 20px',
                borderRadius: 999,
                background: 'var(--coral-soft)',
                color: 'var(--coral)',
                fontWeight: 600,
                fontSize: 15,
                display: 'inline-block',
              }}
            >
              You're on the list — welcome aboard!
            </div>
          ) : (
            <form
              onSubmit={(e) => {
                e.preventDefault()
                if (email.trim()) setSubmitted(true)
              }}
              style={{
                display: 'flex',
                gap: 10,
                maxWidth: 440,
                margin: '0 auto',
                flexWrap: 'wrap',
                justifyContent: 'center',
              }}
            >
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@email.com"
                style={{
                  flex: '1 1 240px',
                  padding: '14px 20px',
                  borderRadius: 999,
                  border: '1px solid var(--line)',
                  fontSize: 15,
                  outline: 'none',
                }}
              />
              <button
                type="submit"
                style={{
                  background: 'var(--navy)',
                  color: '#fff',
                  padding: '14px 26px',
                  borderRadius: 999,
                  border: 'none',
                  fontWeight: 600,
                  fontSize: 15,
                  cursor: 'pointer',
                }}
              >
                Subscribe
              </button>
            </form>
          )}
        </div>

        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            flexWrap: 'wrap',
            gap: 20,
            paddingTop: 32,
            borderTop: '1px solid var(--line)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, fontWeight: 700 }}>
            <span
              style={{
                width: 28,
                height: 28,
                borderRadius: '50%',
                background: 'var(--navy)',
                color: '#fff',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: 10,
                fontWeight: 800,
              }}
            >
              180
            </span>
            180° Consulting Newsletter
          </div>

          <div style={{ display: 'flex', gap: 24, fontSize: 14 }}>
            <a href="#top" style={{ color: 'var(--ink-soft)', textDecoration: 'none' }}>
              Back to top
            </a>
            <a href="#" style={{ color: 'var(--ink-soft)', textDecoration: 'none' }}>
              Privacy
            </a>
            <a href="#" style={{ color: 'var(--ink-soft)', textDecoration: 'none' }}>
              Archive
            </a>
          </div>

          <div style={{ display: 'flex', gap: 14 }}>
            {['LinkedIn', 'Instagram', 'X'].map((s) => (
              <a
                key={s}
                href="#"
                aria-label={s}
                style={{
                  width: 34,
                  height: 34,
                  borderRadius: '50%',
                  border: '1px solid var(--line)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: 12,
                  color: 'var(--ink-soft)',
                  textDecoration: 'none',
                }}
              >
                {s[0]}
              </a>
            ))}
          </div>
        </div>

        <p style={{ textAlign: 'center', fontSize: 13, color: 'var(--ink-soft)', marginTop: 32 }}>
          © {new Date().getFullYear()} 180 Degrees Consulting — a student-run,
          non-profit organisation. Not affiliated with any single chapter.
        </p>
      </div>
    </footer>
  )
}
