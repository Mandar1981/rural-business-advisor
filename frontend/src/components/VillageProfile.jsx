import React from 'react'

const fmt = n => (n === null || n === undefined ? '-' : Number(n).toLocaleString())

export default function VillageProfile({ village }) {
  if (!village) return null
  return (
    <div className="card">
      <div className="flex-between">
        <h2>Village Digital Profile</h2>
        <span className="badge info">Village-level data</span>
      </div>
      <p className="small" style={{ marginTop: 0 }}>
        <strong>{village.village}</strong> - {village.district}
      </p>
      <div className="grid cols-4">
        <div className="stat"><div className="stat-label">Population</div><div className="stat-value">{fmt(village.population)}</div></div>
        <div className="stat"><div className="stat-label">Households</div><div className="stat-value">{fmt(village.households)}</div></div>
        <div className="stat"><div className="stat-label">Total Workers</div><div className="stat-value">{fmt(village.total_workers)}</div></div>
        <div className="stat"><div className="stat-label">Non-Workers</div><div className="stat-value">{fmt(village.non_workers)}</div></div>
      </div>
      <h3 style={{ marginTop: 18 }}>Workforce Breakdown</h3>
      <table className="tbl">
        <thead><tr><th>Category</th><th>Main</th><th>Marginal</th></tr></thead>
        <tbody>
          <tr><td>Cultivators</td><td>{fmt(village.main_cultivators)}</td><td>{fmt(village.marginal_cultivators)}</td></tr>
          <tr><td>Agricultural Labourers</td><td>{fmt(village.main_agri_labourers)}</td><td>{fmt(village.marginal_agri_labourers)}</td></tr>
          <tr><td>Household Industry</td><td>{fmt(village.main_hh_industry)}</td><td>{fmt(village.marginal_hh_industry)}</td></tr>
          <tr><td>Other Workers</td><td>{fmt(village.main_other_workers)}</td><td>{fmt(village.marginal_other_workers)}</td></tr>
        </tbody>
      </table>
    </div>
  )
}
