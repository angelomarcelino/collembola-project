import { useState, useMemo, useEffect } from 'react'
import { AnimalCard } from '../components/AnimalCard'

export function Catalog() {
  const [animals, setAnimals] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [search, setSearch] = useState('')

  useEffect(() => {
    // We assume data/animals.json is accessible from the public folder
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
    <>
      <header className="header">
        <div className="header__inner">
          <h1 className="header__title">Catálogo de Colêmbolos</h1>
          <p className="header__subtitle">
            Catálogo interativo de espécies de colêmbolos do Brasil e do mundo
          </p>
          {!loading && !error && (
            <div className="header__stats">
              <div className="header__stat">
                <span className="header__stat-value">{animals.length}</span>
                espécies
              </div>
              <div className="header__stat">
                <span className="header__stat-value">{uniqueFamilies}</span>
                famílias
              </div>
              <div className="header__stat">
                <span className="header__stat-value">{uniqueCountries}</span>
                distribuições
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
            placeholder="Buscar por nome, família, estado, habitat..."
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
          <p className="error__title">Falha ao carregar os dados</p>
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
                Nenhuma espécie encontrada para &ldquo;{search}&rdquo;
              </p>
            </div>
          )}
        </main>
      )}
    </>
  )
}
