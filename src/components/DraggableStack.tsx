import { useState } from 'react'
import { motion } from 'framer-motion'
import Photo from './Photo'

type StackItem = { caption: string; src?: string; fit?: 'cover' | 'contain' }

export default function DraggableStack({ items, label }: { items: StackItem[]; label: string }) {
  const [order, setOrder] = useState(items.map((_, i) => i))
  const bringForward = (index: number) => setOrder(previous => [...previous.filter(i => i !== index), index])

  return (
    <div className="photo-stack" aria-label={label}>
      {items.map((item, index) => (
        <motion.div
          key={item.caption}
          drag
          dragMomentum={false}
          onPointerDown={() => bringForward(index)}
          onKeyDown={event => { if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); bringForward(index) } }}
          role="button"
          tabIndex={0}
          aria-label={`Move ${item.caption} to the front`}
          style={{
            position: 'absolute',
            width: '100%',
            top: `${index * 9}px`,
            left: `${index * 5}px`,
            rotate: [-8, 6, -3, 4][index % 4],
            zIndex: order.indexOf(index) + 1,
            padding: 10,
            border: '1px solid var(--red)',
            background: 'var(--cream)',
            boxShadow: '11px 13px 0 rgba(75, 53, 44, 0.23)',
            cursor: 'grab',
            touchAction: 'none',
            userSelect: 'none',
          }}
          whileDrag={{ cursor: 'grabbing' }}
        >
          <Photo {...item} index={index} draggable={false} />
        </motion.div>
      ))}
      <span className="caps stack-hint">Drag the images to explore</span>
      <style>{`.photo-stack { position: relative; width: min(38vw, 470px); height: 440px; } .stack-hint { position: absolute; bottom: -30px; left: 0; white-space: nowrap; font-size: 10px; } .photo-stack img { pointer-events: none; -webkit-user-drag: none; } @media(max-width:800px){ .photo-stack { width: min(76vw, 360px); height: 350px; } }`}</style>
    </div>
  )
}
