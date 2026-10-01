import { motion } from 'framer-motion'

const TONES = ['#ff4552', '#ff6f78', '#f0303e', '#ff8a91', '#e8283a']

export default function Photo({
  src,
  caption,
  index = 0,
  ratio = '4/3',
  fit = 'cover',
}: {
  src?: string
  caption: string
  index?: number
  ratio?: string
  fit?: 'cover' | 'contain'
}) {
  return (
    <motion.figure
      initial={{ opacity: 0, y: 40 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-10%' }}
      transition={{ duration: 0.7, delay: (index % 3) * 0.1 }}
      style={{ margin: 0 }}
    >
      <div
        style={{
          aspectRatio: ratio,
          overflow: 'hidden',
          background: src && fit === 'contain' ? '#fff' : TONES[index % TONES.length],
          position: 'relative',
        }}
      >
        {src ? (
          <img src={src} alt={caption} style={{ width: '100%', height: '100%', objectFit: fit, padding: fit === 'contain' ? '8%' : 0, display: 'block' }} />
        ) : (
          <div
            style={{
              position: 'absolute',
              inset: 0,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'var(--cream)',
              fontSize: 11,
              letterSpacing: '0.3em',
              textTransform: 'uppercase',
              opacity: 0.8,
            }}
          >
            Photo coming soon
          </div>
        )}
      </div>
      <figcaption style={{ fontSize: 13, marginTop: 12, lineHeight: 1.45, maxWidth: 360 }}>{caption}</figcaption>
    </motion.figure>
  )
}
