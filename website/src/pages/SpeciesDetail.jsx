import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { ChevronLeft, Info, MapPin } from 'lucide-react'
import { BrazilMap } from '../components/BrazilMap'

export function SpeciesDetail() {
  const { id } = useParams()
  const [animal, setAnimal] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [imgError, setImgError] = useState(false)

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}data/animals.json`)
      .then((res) => {
        if (!res.ok) throw new Error(`Failed to load data`)
        return res.json()
      })
      .then((data) => {
        const found = data.find((a) => a.id === id)
        if (found) {
          setAnimal(found)
        } else {
          setError('Espécie não encontrada.')
        }
        setLoading(false)
      })
      .catch((err) => {
        setError(err.message)
        setLoading(false)
      })
  }, [id])

  if (loading) {
    return (
      <div className="loading" style={{ height: '50vh' }}>
        <div className="loading__spinner" />
      </div>
    )
  }

  if (error || !animal) {
    return (
      <div className="error" style={{ marginTop: '2rem' }}>
        <p className="error__title">Erro</p>
        <p className="error__message">{error}</p>
        <Link to="/" className="back-link">
          <ChevronLeft size={20} /> Voltar para o Catálogo
        </Link>
      </div>
    )
  }

  return (
    <main className="detail-page">
      <nav className="detail-nav">
        <Link to="/" className="back-link">
          <ChevronLeft size={20} /> Voltar
        </Link>
      </nav>

      <article className="detail-content">
        <div className="detail-left-column">
          <div className="detail-image-section">
            {!imgError && animal.image ? (
              <img
                className="detail-image"
                src={`${import.meta.env.BASE_URL}${animal.image}`}
                alt={animal.scientific_name}
                loading="lazy"
                onError={() => setImgError(true)}
              />
            ) : (
              <div className="detail-image-placeholder">
                <span className="placeholder-icon">🔬</span>
                <p>Imagem indisponível</p>
              </div>
            )}
          </div>

          <section className="info-block map-block-left">
            <h3 className="info-title"><MapPin size={18}/> Distribuição Geográfica</h3>
            <p className="detail-text">{animal.country}</p>
            <div className="map-container">
               <BrazilMap distributionText={animal.country} />
            </div>
          </section>
        </div>

        <div className="detail-info-section">
          <header className="detail-header">
            <h1 className="detail-title">{animal.scientific_name}</h1>
            {animal.common_name !== 'Collembola' && animal.common_name !== 'Springtail' && (
              <p className="detail-subtitle">{animal.common_name}</p>
            )}
            <span className={`animal-card__status-badge status--${animal.conservation_status.toLowerCase()} detail-status`}>
              {animal.conservation_status}
            </span>
          </header>

          <section className="info-block">
            <h3 className="info-title"><Info size={18}/> Classificação Científica</h3>
            <div className="taxonomy-grid">
              <div className="taxonomy-item">
                <span className="taxonomy-label">Classe</span>
                <span className="taxonomy-value">{animal.class}</span>
              </div>
              <div className="taxonomy-item">
                <span className="taxonomy-label">Ordem</span>
                <span className="taxonomy-value">{animal.order}</span>
              </div>
              <div className="taxonomy-item">
                <span className="taxonomy-label">Família</span>
                <span className="taxonomy-value">{animal.family}</span>
              </div>
            </div>
          </section>

          <section className="info-block">
            <h3 className="info-title">Sobre a Espécie</h3>
            <p className="detail-description">{animal.description}</p>
          </section>

          {animal.bibliography && (
            <section className="info-block">
              <h3 className="info-title">Referências Bibliográficas</h3>
              <p className="detail-description" style={{ fontSize: '0.9rem', color: 'var(--text-color-secondary)' }}>
                {animal.bibliography}
              </p>
            </section>
          )}
        </div>
      </article>
    </main>
  )
}
