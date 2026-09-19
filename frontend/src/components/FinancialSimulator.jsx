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

export default function FinancialSimulator({ onResult }) {
  const [form, setForm] = useState(defaults)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const run = async () => {
    setLoading(true); setError('')
    try {
      const r = await api.financial({
        initial_investment: Number(form.initial_investment),
        selling_price_per_unit: Number(form.selling_price_per_unit),
        units_per_month: Number(form.units_per_month),
        monthly_fixed_cost: Number(form.monthly_fixed_cost),
        variable_cost_per_unit: Number(form.variable_cost_per_unit),
      })
      setResult(r)
      if (onResult) onResult(r, form)
    } catch (e) { setError(e.message) }
    finally { setLoading(false) }
  }

  useEffect(() => { run() }, []) // eslint-disable-line

  const set = k => e => setForm({ ...form, [k]: e.target.value })

  return (
    <div className="card">
      <h2>Financial Feasibility Calculator</h2>
      <p className="small" style={{ marginTop: 0 }}>Based on user assumptions. Not a guaranteed prediction.</p>
      <div className="grid cols-2">
        <div className="form-row"><label>Initial Investment (Rs.)</label><input type="number" value={form.initial_investment} onChange={set('initial_investment')} /></div>
        <div className="form-row"><label>Selling Price per Unit (Rs.)</label><input type="number" value={form.selling_price_per_unit} onChange={set('selling_price_per_unit')} /></div>
        <div className="form-row"><label>Units Sold per Month</label><input type="number" value={form.units_per_month} onChange={set('units_per_month')} /></div>
        <div className="form-row"><label>Monthly Fixed Cost (Rs.)</label><input type="number" value={form.monthly_fixed_cost} onChange={set('monthly_fixed_cost')} /></div>
        <div className="form-row"><label>Variable Cost per Unit (Rs.)</label><input type="number" value={form.variable_cost_per_unit} onChange={set('variable_cost_per_unit')} /></div>
      </div>
      <button className="btn" onClick={run} disabled={loading}>{loading ? 'Calculating...' : 'Recalculate'}</button>
      {error && <div className="error-banner" style={{ marginTop: 14 }}>{error}</div>}
      {result && (
        <>
          <h3 style={{ marginTop: 18 }}>Results</h3>
          <div className="grid cols-3">
            <div className="stat"><div className="stat-label">Monthly Revenue</div><div className="stat-value">{inr(result.monthly_revenue)}</div></div>
            <div className="stat"><div className="stat-label">Total Monthly Cost</div><div className="stat-value">{inr(result.total_monthly_cost)}</div></div>
            <div className="stat"><div className="stat-label">Monthly Profit</div><div className="stat-value">{inr(result.monthly_profit)}</div></div>
            <div className="stat"><div className="stat-label">Annual Profit</div><div className="stat-value">{inr(result.annual_profit)}</div></div>
            <div className="stat"><div className="stat-label">ROI</div><div className="stat-value">{result.roi_percent}%</div></div>
            <div className="stat"><div className="stat-label">Break-even Quantity</div><div className="stat-value">{result.break_even_quantity ?? '-'}</div></div>
            <div className="stat"><div className="stat-label">Break-even Revenue</div><div className="stat-value">{inr(result.break_even_revenue)}</div></div>
            <div className="stat"><div className="stat-label">Payback (months)</div><div className="stat-value">{result.payback_period_months ?? '-'}</div></div>
          </div>
          {result.break_even_note && <div className="notice" style={{ marginTop: 12 }}>{result.break_even_note}</div>}
          {result.payback_note && <div className="notice" style={{ marginTop: 6 }}>{result.payback_note}</div>}
          <div className="notice info" style={{ marginTop: 12 }}>{result.assumptions_note}</div>
        </>
      )}
    </div>
  )
}
