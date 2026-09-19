import React from 'react'

export default function MLResult({ ml }) {
  if (!ml) return null
  return (
    <div className="card">
      <div className="flex-between">
        <h2>Random Forest Proxy Prediction</h2>
        <span className="badge warn">Proxy labels</span>
      </div>
      <div className="grid cols-2">
        <div className="stat">
          <div className="stat-label">Predicted Category</div>
          <div className="stat-value" style={{ fontSize: 16 }}>{ml.predicted_category}</div>
        </div>
        <div className="stat">
          <div className="stat-label">Confidence</div>
          <div className="stat-value">{(ml.confidence * 100).toFixed(1)}%</div>
        </div>
      </div>
      <div className="notice">{ml.disclaimer}</div>
    </div>
  )
}
