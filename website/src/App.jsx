import { HashRouter as Router, Routes, Route, useLocation } from 'react-router-dom'
import { Catalog } from './pages/Catalog'
import { SpeciesDetail } from './pages/SpeciesDetail'
import './App.css'

function AppContent() {
  const location = useLocation()
  const isDetailPage = location.pathname.startsWith('/species/')

  return (
    <div className={`app ${isDetailPage ? 'app--detail' : ''}`}>
      <Routes>
        <Route path="/" element={<Catalog />} />
        <Route path="/species/:id" element={<SpeciesDetail />} />
      </Routes>
      <footer className="footer">
        Collembola Project &middot; Dados obtidos via scraping automatizado
      </footer>
    </div>
  )
}

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  )
}

export default App