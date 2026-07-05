import React, { useMemo } from 'react'
import { BrazilSVG } from './BrazilSVG'

// Dictionary of state codes and their normalized names for matching
const STATE_MAP = {
  'Acre': 'AC',
  'Alagoas': 'AL',
  'Amapá': 'AP',
  'Amazonas': 'AM',
  'Bahia': 'BA',
  'Ceará': 'CE',
  'Distrito Federal': 'DF',
  'Espírito Santo': 'ES',
  'Goiás': 'GO',
  'Maranhão': 'MA',
  'Mato Grosso': 'MT',
  'Mato Grosso do Sul': 'MS',
  'Minas Gerais': 'MG',
  'Pará': 'PA',
  'Paraíba': 'PB',
  'Paraná': 'PR',
  'Pernambuco': 'PE',
  'Piauí': 'PI',
  'Rio de Janeiro': 'RJ',
  'Rio Grande do Norte': 'RN',
  'Rio Grande do Sul': 'RS',
  'Rondônia': 'RO',
  'Roraima': 'RR',
  'Santa Catarina': 'SC',
  'São Paulo': 'SP',
  'Sergipe': 'SE',
  'Tocantins': 'TO'
}

export function BrazilMap({ distributionText = '' }) {
  // Normalize the distribution text and find active state acronyms
  const activeStates = useMemo(() => {
    const active = new Set()
    const text = distributionText.toLowerCase()
    const normalizedText = text.normalize("NFD").replace(/[\u0300-\u036f]/g, "")
    
    // Check for explicit state names
    Object.entries(STATE_MAP).forEach(([stateName, stateCode]) => {
      const normalizedStateName = stateName.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase()
      if (normalizedText.includes(normalizedStateName) || normalizedText.includes(` ${stateCode.toLowerCase()} `) || normalizedText.includes(`(${stateCode.toLowerCase()})`) || normalizedText.includes(`, ${stateCode.toLowerCase()},`)) {
        active.add(stateCode)
      }
    })
    return active
  }, [distributionText])

  const isBrazil = distributionText.toLowerCase().includes('brazil')

  if (!isBrazil) {
    return <div className="distribution-note">Ocorrência fora do Brasil Continental ou dados insuficientes.</div>
  }

  return (
    <div className="brazil-map-wrapper">
      <div className="brazil-map-svg-container">
        <BrazilSVG activeStates={activeStates} />
      </div>
      <div className="brazil-map-states">
        {Array.from(activeStates).map(stateCode => (
          <span key={stateCode} className="state-chip state-chip--active" style={{ background: 'var(--color-accent)' }}>
            {stateCode}
          </span>
        ))}
      </div>
    </div>
  )
}
