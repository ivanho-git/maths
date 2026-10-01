import { useState } from 'react'
import { motion } from 'framer-motion'
import { HeartBubble, Mug, Sparkle } from './Doodles'

export default function Footer() {
  const [email, setEmail] = useState('')
  const [done, setDone] = useState(false)

  return (
    <footer id="subscribe">
      <div className="wrap">
        <div style={{ background: 'var(--ink)', color: '#fff', borderRadius: 28, padding: '100px 48px 80px', margin: '120px 0 40px', textAlign: 'center', position: 'relative', overflow: 'hidden' }}>
          <HeartBubble size={100} style={{ position: 'absolute', left: '6%', top: 50, animation: 'bob 5s ease-in-out infinite' }} />
          <Mug size={80} style={{ position: 'absolute', right: '7%', bottom: 50, animation: 'bob 6s ease-in-out infinite' }} />
          <Sparkle size={40} style={{ position: 'absolute', right: '18%', top: 60, animation: 'bob 4s ease-in-out infinite' }} />
          <div className="serif" style={{ fontSize: 'clamp(56px, 10vw, 150px)' }}>
            {['Never miss', 'an issue'].map((t, i) => (
              <motion.div
                key={t}
                initial={{ opacity: 0, x: i ? 80 : -80 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.9, ease: [0.22, 1, 0.36, 1] }}
                style={{ textAlign: 'center', color: i ? 'var(--lilac)' : '#fff' }}
              >
                {t}
              </motion.div>
            ))}
          </div>

          {done ? (
            <div style={{ position: 'relative' }}>
              {Array.from({ length: 36 }).map((_, k) => (
                <motion.span
                  key={k}
                  initial={{ x: 0, y: 0, opacity: 1, rotate: 0 }}
                  animate={{ x: Math.cos(k * 0.7) * (120 + (k % 5) * 40), y: Math.sin(k * 0.7) * (80 + (k % 4) * 30) - 60, opacity: 0, rotate: k * 40 }}
                  transition={{ duration: 1.4, ease: 'easeOut' }}
                  style={{ position: 'absolute', left: '50%', top: 30, width: 12, height: 12, borderRadius: k % 3 ? 2 : 6, background: ['var(--green)', 'var(--lilac)', '#fff'][k % 3], border: '1.5px solid var(--ink)' }}
                />
              ))}
              <motion.p initial={{ scale: 0.6, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} transition={{ type: 'spring', stiffness: 300, damping: 12 }} className="serif" style={{ fontSize: 34, marginTop: 56 }}>You're in! See you in your inbox 🎉</motion.p>
            </div>
          ) : (
            <form
              onSubmit={(e) => {
                e.preventDefault()
                if (email.trim()) setDone(true)
              }}
              style={{ display: 'flex', gap: 14, margin: '56px auto 0', flexWrap: 'wrap', maxWidth: 620, justifyContent: 'center' }}
            >
              <input
                type="email"
                required
                placeholder="Your email address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                style={{
                  flex: '1 1 280px',
                  background: 'transparent',
                  border: 'none',
                  borderBottom: '1px solid #fff',
                  color: '#fff',
                  fontSize: 18,
                  padding: '14px 0',
                  outline: 'none',
                }}
              />
              <button type="submit" className="pill">Subscribe →</button>
            </form>
          )}
        </div>

        <div
          style={{
            borderTop: '1px solid var(--red)',
            padding: '48px 0',
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
            gap: 32,
            fontSize: 14,
            lineHeight: 1.6,
          }}
        >
          <div style={{ display: 'flex', gap: 14, alignItems: 'flex-start' }}>
            <img src="/images/180dc-logo-full.png" alt="180 Degrees Consulting" width={110} style={{ borderRadius: 10, background: "#fff", padding: 6 }} />
            <div>
              <strong>180 Degrees Consulting</strong>
              <br />
              The student-run consultancy
              <br />
              for social impact
            </div>
          </div>
          <nav style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            {['Past issues', 'Privacy policy', 'Contact the editors'].map((l) => (
              <a key={l} href="#" style={{ color: 'var(--red)', textDecoration: 'none' }}>{l}</a>
            ))}
          </nav>
          <div style={{ display: 'flex', gap: 12, justifyContent: 'flex-end', alignItems: 'flex-start' }}>
            {['in', 'ig', 'x'].map((s) => (
              <a
                key={s}
                href="#"
                aria-label={s}
                style={{
                  width: 40,
                  height: 40,
                  borderRadius: '50%',
                  border: '1px solid var(--red)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'var(--red)',
                  textDecoration: 'none',
                  fontWeight: 600,
                }}
              >
                {s}
              </a>
            ))}
          </div>
        </div>
      </div>
    </footer>
  )
}
