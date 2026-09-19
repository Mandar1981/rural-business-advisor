import React from 'react'

export default function BudgetInput({ value, onChange }) {
  return (
    <div className="form-row">
      <label>Available Budget (Rs.)</label>
      <input type="number" min="1000" step="1000" placeholder="e.g. 200000"
        value={value} onChange={e => onChange(e.target.value)} />
    </div>
  )
}
