import { useEffect, useRef, useState } from 'react'
import Photo from './Photo'

type GalleryItem = { caption: string; src?: string; fit?: 'cover' | 'contain' }

export default function DragGallery({ items, label }: { items: GalleryItem[]; label: string }) {
  const track = useRef<HTMLDivElement>(null)
  const gesture = useRef<{ x: number; scroll: number; lastX: number; lastTime: number; velocity: number } | null>(null)
  const animation = useRef<number | null>(null)
  const [dragging, setDragging] = useState(false)
  const [active, setActive] = useState(0)

  useEffect(() => {
    const el = track.current
    if (!el) return
    const center = () => { el.scrollLeft = (el.children[items.length] as HTMLElement).offsetLeft - (el.children[0] as HTMLElement).offsetLeft }
    center()
    const observer = new ResizeObserver(center)
    observer.observe(el)
    return () => {
      observer.disconnect()
      if (animation.current !== null) cancelAnimationFrame(animation.current)
    }
  }, [items])

  const wrap = () => {
    const el = track.current
    if (!el) return
    const cycle = (el.children[items.length] as HTMLElement).offsetLeft - (el.children[0] as HTMLElement).offsetLeft
    if (el.scrollLeft < cycle * 0.5) el.scrollLeft += cycle
    if (el.scrollLeft > cycle * 1.5) el.scrollLeft -= cycle
    const first = el.children[0] as HTMLElement | undefined
    if (first) {
      const step = first.offsetWidth + 28
      setActive(((Math.round((el.scrollLeft - cycle) / step) % items.length) + items.length) % items.length)
    }
  }

  const stopMomentum = () => {
    if (animation.current !== null) cancelAnimationFrame(animation.current)
    animation.current = null
  }

  const onPointerDown = (event: React.PointerEvent<HTMLDivElement>) => {
    if (event.pointerType === 'touch') return
    const el = track.current
    if (!el) return
    stopMomentum()
    el.setPointerCapture(event.pointerId)
    gesture.current = { x: event.clientX, scroll: el.scrollLeft, lastX: event.clientX, lastTime: performance.now(), velocity: 0 }
    setDragging(true)
  }

  const onPointerMove = (event: React.PointerEvent<HTMLDivElement>) => {
    const el = track.current
    const state = gesture.current
    if (!el || !state) return
    const now = performance.now()
    const dt = now - state.lastTime
    if (dt > 0) state.velocity = (state.lastX - event.clientX) / dt
    state.lastX = event.clientX
    state.lastTime = now
    el.scrollLeft = state.scroll + state.x - event.clientX
    wrap()
    state.scroll = el.scrollLeft - state.x + event.clientX
  }

  const onPointerUp = (event: React.PointerEvent<HTMLDivElement>) => {
    const el = track.current
    const state = gesture.current
    if (!el || !state) return
    if (el.hasPointerCapture(event.pointerId)) el.releasePointerCapture(event.pointerId)
    gesture.current = null
    setDragging(false)
    let velocity = state.velocity * 16
    const coast = () => {
      velocity *= 0.92
      if (Math.abs(velocity) < 0.3) { animation.current = null; return }
      el.scrollLeft += velocity
      wrap()
      animation.current = requestAnimationFrame(coast)
    }
    if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) animation.current = requestAnimationFrame(coast)
  }

  const step = (direction: number) => {
    const el = track.current
    if (!el) return
    stopMomentum()
    const card = el.children[0] as HTMLElement | undefined
    el.scrollBy({ left: direction * ((card?.offsetWidth ?? 300) + 28), behavior: 'smooth' })
  }

  return (
    <div style={{ marginTop: 90 }}>
      <div
        ref={track}
        aria-label={label}
        className="drag-gallery no-scrollbar"
        onPointerDown={onPointerDown}
        onPointerMove={onPointerMove}
        onPointerUp={onPointerUp}
        onPointerCancel={onPointerUp}
        onScroll={wrap}
        style={{ display: 'grid', gridAutoFlow: 'column', gridAutoColumns: 'minmax(270px, 42%)', gap: 28, overflowX: 'auto', cursor: dragging ? 'grabbing' : 'grab', touchAction: 'pan-x pan-y', userSelect: 'none' }}
      >
        {[...items, ...items, ...items].map((item, index) => (
          <div key={`${index}-${item.caption}`} aria-hidden={index < items.length || index >= items.length * 2}>
            <Photo {...item} index={index % items.length} draggable={false} />
          </div>
        ))}
      </div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: 24 }}>
        <span className="caps" style={{ fontSize: 10 }}>Drag to explore · {active + 1} / {items.length}</span>
        <div style={{ display: 'flex', gap: 10 }}>
          <button type="button" className="gallery-arrow" aria-label={`Previous ${label} image`} onClick={() => step(-1)}>←</button>
          <button type="button" className="gallery-arrow" aria-label={`Next ${label} image`} onClick={() => step(1)}>→</button>
        </div>
      </div>
      <style>{`.drag-gallery img { pointer-events: none; -webkit-user-drag: none; } .gallery-arrow { width: 46px; height: 46px; border: 1px solid var(--red); border-radius: 50%; color: var(--red); background: transparent; cursor: pointer; font-size: 20px; } .gallery-arrow:hover { background: var(--red); color: var(--cream); } @media(max-width:700px) { .drag-gallery { grid-auto-columns: minmax(245px, 80%) !important; } }`}</style>
    </div>
  )
}
