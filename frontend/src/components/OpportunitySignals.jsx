import React from 'react'

export default function OpportunitySignals({ signals }) {
  return (
    <div className="card">
      <div className="flex-between">
        <h2>Opportunity Signals</h2>
        <span className="badge info">Not proof of market demand</span>
      </div>
      {(!signals || signals.length === 0) && (
        <p className="small">No strong opportunity signals detected from available data.</p>
      )}
      {signals?.map((s, i) => (
        <div key={i} className="signal-row">
          <div className="signal-title">{s.signal}</div>
          <div className="signal-evidence">{s.evidence}</div>
          <div className="small" style={{ marginTop: 4 }}>
            Related category: <strong>{s.related_business_category}</strong>
          </div>
        </div>
      ))}
    </div>
  )
}
