import { useState } from 'react'
import { Link } from 'react-router-dom'

const STATUS_LABELS = {
  EX: 'Extinta',
  EW: 'Extinta na Natureza',
  CR: 'Criticamente Ameaçada',
  EN: 'Em Perigo',
  VU: 'Vulnerável',
  NT: 'Quase Ameaçada',
  LC: 'Pouco Preocupante',
  DD: 'Dados Insuficientes',
  NE: 'Não Avaliada',
}

export function AnimalCard({ animal }) {
  const [imgError, setImgError] = useState(false)
  const statusClass = `status--${animal.conservation_status.toLowerCase()}`
  const statusLabel = STATUS_LABELS[animal.conservation_status] || animal.conservation_status

  return (
    <Link to={`/species/${animal.id}`} className="animal-card" id={`card-${animal.id}`}>
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
          <span className="animal-card__tag">📍 {animal.country.substring(0, 20)}{animal.country.length > 20 ? '...' : ''}</span>
          <span className="animal-card__tag">🌿 {animal.habitat}</span>
        </div>

        <p className="animal-card__description">
          {animal.description}
        </p>
      </div>
    </Link>
  )
}
