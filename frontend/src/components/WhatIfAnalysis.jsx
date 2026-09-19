import React, { useEffect, useState } from 'react'
import { api } from '../services/api.js'

const defaults = {
  initial_investment: 200000,
  selling_price_per_unit: 50,
  units_per_month: 1000,
  monthly_fixed_cost: 15000,
  variable_cost_per_unit: 20,
}

const inr = n => (n === null || n === undefined ? '-' : `Rs. ${Number(n).toLocaleString()}`)

export default function WhatIfAnalysis({ initialForm }) {
  const [form] = useState(initialForm || defaults)
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const run = async () => {
    setLoading(true); setError('')
    try {
      const r = await api.whatIf({
        initial_investment: Number(form.initial_investment),
        selling_price_per_unit: Number(form.selling_price_per_unit),
        units_per_month: Number(form.units_per_month),
        monthly_fixed_cost: Number(form.monthly_fixed_cost),
        variable_cost_per_unit: Number(form.variable_cost_per_unit),
      })
      setData(r)
    } catch (e) { setError(e.message) }
    finally { setLoading(false) }
  }

  useEffect(() => { run() }, []) // eslint-disable-line

  return (
    <div className="card">
      <h2>What-if Scenarios</h2>
      <p className="small" style={{ marginTop: 0 }}>Scenario-based assumptions - not guaranteed predictions.</p>
      <button className="btn" onClick={run} disabled={loading}>{loading ? 'Running...' : 'Run Scenarios'}</button>
      {error && <div className="error-banner" style={{ marginTop: 12 }}>{error}</div>}
      {data && (
        <table className="tbl" style={{ marginTop: 14 }}>
          <thead>
            <tr><th>Scenario</th><th>Revenue</th><th>Profit / Month</th><th>ROI</th><th>Break-even Qty</th><th>Payback (months)</th></tr>
          </thead>
          <tbody>
            {['conservative', 'expected', 'optimistic'].map(k => {
              const s = data[k]; const r = s.results
              return (
                <tr key={k}>
                  <td>{s.label}</td>
                  <td>{inr(r.monthly_revenue)}</td>
                  <td>{inr(r.monthly_profit)}</td>
                  <td>{r.roi_percent}%</td>
                  <td>{r.break_even_quantity ?? '-'}</td>
                  <td>{r.payback_period_months ?? '-'}</td>
                </tr>
              )
            })}
          </tbody>
        </table>
      )}
      {data && <div className="notice info" style={{ marginTop: 10 }}>{data.note}</div>}
    </div>
  )
}
