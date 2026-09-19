import React from 'react'

const inr = n => `Rs. ${Number(n).toLocaleString()}`

export default function PMEGPCard({ pmegp }) {
  if (!pmegp) return null
  return (
    <div className="card">
      <h2>{pmegp.scheme_name}</h2>
      <p>{pmegp.potential_relevance}</p>
      <div className="grid cols-2">
        <div className="stat"><div className="stat-label">User Budget</div><div className="stat-value">{inr(pmegp.user_budget)}</div></div>
        <div className="stat"><div className="stat-label">Estimated Funding Gap</div><div className="stat-value">{inr(pmegp.estimated_funding_gap)}</div></div>
      </div>
      <h3 style={{ marginTop: 14 }}>Eligibility Checklist (verify officially)</h3>
      <ul>{pmegp.checklist.map((c, i) => <li key={i}>{c}</li>)}</ul>
      <div className="notice danger">{pmegp.verification_warning}</div>
    </div>
  )
}
