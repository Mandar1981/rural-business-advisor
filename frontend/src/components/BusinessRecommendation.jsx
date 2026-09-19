import React from 'react'

const inr = n => `Rs. ${Number(n).toLocaleString()}`

export default function BusinessRecommendation({ recommendations }) {
  if (!recommendations?.length) return null
  return (
    <div className="card">
      <h2>Business Recommendations</h2>
      <p className="small" style={{ marginTop: 0 }}>
        Ranked by opportunity score. Startup costs are prototype/domain estimates - not official figures.
      </p>
      {recommendations.map((r, i) => (
        <div key={i} className={`reco-card ${r.budget_fit === 'Fits budget' ? '' : 'budget-bad'}`}>
          <div className="reco-title">
            <h3>{r.business_category}</h3>
            <span className={`badge ${r.budget_fit === 'Fits budget' ? 'ok' : 'warn'}`}>{r.budget_fit}</span>
          </div>
          <p className="small" style={{ marginTop: 4 }}>Suggested sub-business: <strong>{r.sub_business}</strong></p>
          <div className="reco-meta">
            <div><span>Opportunity Score: </span><strong>{(r.opportunity_score * 100).toFixed(1)}</strong></div>
            <div><span>Estimated Investment: </span><strong>{inr(r.estimated_investment)}</strong></div>
            <div><span>Funding Gap: </span><strong>{inr(r.funding_gap)}</strong></div>
          </div>
          <div style={{ marginTop: 10 }}>
            <strong style={{ fontSize: 13 }}>Why recommended:</strong>
            <ul style={{ marginTop: 4 }}>{r.why_recommended.map((w, j) => <li key={j} style={{ fontSize: 13 }}>{w}</li>)}</ul>
          </div>
          <p className="small">{r.cost_note}</p>
        </div>
      ))}
    </div>
  )
}
