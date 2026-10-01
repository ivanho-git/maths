import Header from './components/Header'
import Hero from './components/Hero'
import Coverage from './components/Coverage'
import Process from './components/Process'
import Differentiators from './components/Differentiators'
import Footer from './components/Footer'
import Articles from './components/Articles'

function App() {
  const isArticles = window.location.pathname.replace(/\/$/, '') === '/articles'

  return (
    <>
      <Header />
      {isArticles ? (
        <Articles />
      ) : (
        <>
          <Hero />
          <Coverage />
          <Process />
          <Differentiators />
        </>
      )}
      <Footer />
    </>
  )
}

export default App
