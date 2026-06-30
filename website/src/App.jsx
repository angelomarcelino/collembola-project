import { useState, useEffect, useMemo } from 'react'
import './App.css'

const STATUS_LABELS = {
  EX: 'Extinct',
  EW: 'Extinct in Wild',
  CR: 'Critically Endangered',
  EN: 'Endangered',
  VU: 'Vulnerable',
  NT: 'Near Threatened',
  LC: 'Least Concern',
  DD: 'Data Deficient',
  NE: 'Not Evaluated',
}

function AnimalCard({ animal }) {
  const [imgError, setImgError] = useState(false)
  const statusClass = `status--${animal.conservation_status.toLowerCase()}`
  const statusLabel = STATUS_LABELS[animal.conservation_status] || animal.conservation_status

  return (
    <article className="animal-card" id={`card-${animal.id}`}>
      <div className="animal-card__image-wrapper">
        {!imgError ? (
          <img
            className="animal-card__image"
            src={animal.image}
            alt={animal.scientific_name}
            loading="lazy"
            onError={() => setImgError(true)}
          />
        ) : (
          <div className="animal-card__placeholder">
            <span className="animal-card__placeholder-icon">🔬</span>
          </div>
        )}
        <span className={`animal-card__status-badge ${statusClass}`}>
          {statusLabel}
        </span>
      </div>

      <div className="animal-card__body">
        <h2 className="animal-card__scientific-name">{animal.scientific_name}</h2>
        <p className="animal-card__common-name">{animal.common_name}</p>

        <div className="animal-card__meta">
          <span className="animal-card__tag">📍 {animal.country}</span>
          <span className="animal-card__tag">🌍 {animal.continent}</span>
          <span className="animal-card__tag">🌿 {animal.habitat}</span>
        </div>

        <p className="animal-card__description">{animal.description}</p>
      </div>
    </article>
  )
}

function App() {
  const [animals, setAnimals] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [search, setSearch] = useState('')

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}data/animals.json`)
      .then((res) => {
        if (!res.ok) throw new Error(`Failed to load data (${res.status})`)
        return res.json()
      })
      .then((data) => {
        setAnimals(data)
        setLoading(false)
      })
      .catch((err) => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  const filtered = useMemo(() => {
    if (!search.trim()) return animals
    const q = search.toLowerCase()
    return animals.filter(
      (a) =>
        a.scientific_name.toLowerCase().includes(q) ||
        a.common_name.toLowerCase().includes(q) ||
        a.family.toLowerCase().includes(q) ||
        a.order.toLowerCase().includes(q) ||
        a.country.toLowerCase().includes(q) ||
        a.habitat.toLowerCase().includes(q)
    )
  }, [animals, search])

  const uniqueFamilies = useMemo(
    () => new Set(animals.map((a) => a.family)).size,
    [animals]
  )

  const uniqueCountries = useMemo(
    () => new Set(animals.map((a) => a.country)).size,
    [animals]
  )

  return (
    <div className="app">
      <header className="header">
        <div className="header__inner">
          <h1 className="header__title">Collembola Catalog</h1>
          <p className="header__subtitle">
            Interactive catalog of springtail species worldwide
          </p>
          {!loading && !error && (
            <div className="header__stats">
              <div className="header__stat">
                <span className="header__stat-value">{animals.length}</span>
                species
              </div>
              <div className="header__stat">
                <span className="header__stat-value">{uniqueFamilies}</span>
                families
              </div>
              <div className="header__stat">
                <span className="header__stat-value">{uniqueCountries}</span>
                countries
              </div>
            </div>
          )}
        </div>
      </header>

      <div className="search-bar">
        <div className="search-bar__input-wrapper">
          <span className="search-bar__icon">🔍</span>
          <input
            id="search-input"
            className="search-bar__input"
            type="text"
            placeholder="Search by name, family, country, habitat..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
      </div>

      {loading && (
        <div className="loading">
          <div className="loading__spinner" />
        </div>
      )}

      {error && (
        <div className="error">
          <p className="error__title">Failed to load data</p>
          <p className="error__message">{error}</p>
        </div>
      )}

      {!loading && !error && (
        <main className="cards-grid">
          {filtered.length > 0 ? (
            filtered.map((animal) => (
              <AnimalCard key={animal.id} animal={animal} />
            ))
          ) : (
            <div className="empty-state">
              <span className="empty-state__icon">🔎</span>
              <p className="empty-state__text">
                No species found for &ldquo;{search}&rdquo;
              </p>
            </div>
          )}
        </main>
      )}

      <footer className="footer">
        Collembola Project &middot; Data sourced via automated scraping
      </footer>
    </div>
  )
}

export default App
