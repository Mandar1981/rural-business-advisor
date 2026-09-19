import React from 'react'

const fmt = n => (n === null || n === undefined ? '-' : Number(n).toLocaleString())
const pct = n => (n === null || n === undefined ? '-' : `${Number(n).toFixed(2)}%`)

export default function EconomicContext({ ctx }) {
  if (!ctx) return null
  return (
    <div className="card">
      <div className="flex-between">
        <h2>Economic Context</h2>
        <span className="badge info">District-level context</span>
      </div>
      <p className="small" style={{ marginTop: 0 }}>
        Values below are drawn from datasets labelled by their own administrative level
        (source noted). Where a dataset is district-level, it is shown as district context.
      </p>

      {ctx.workforce && (
        <>
          <h3>Workforce (Census B-04)</h3>
          <div className="grid cols-4">
            <div className="stat"><div className="stat-label">Cultivators</div><div className="stat-value">{pct(ctx.workforce.cultivators_pct)}</div></div>
            <div className="stat"><div className="stat-label">Agri Labourers</div><div className="stat-value">{pct(ctx.workforce.agricultural_labourers_pct)}</div></div>
            <div className="stat"><div className="stat-label">Category B</div><div className="stat-value">{pct(ctx.workforce.category_B_pct)}</div></div>
            <div className="stat"><div className="stat-label">Category C (HHI)</div><div className="stat-value">{pct(ctx.workforce.category_C_HHI_pct)}</div></div>
          </div>
        </>
      )}

      {ctx.occupation && (
        <>
          <h3 style={{ marginTop: 18 }}>Occupation Distribution (Census B-24)</h3>
          <div className="grid cols-3">
            {Object.entries(ctx.occupation).map(([k, v]) => (
              <div key={k} className="stat">
                <div className="stat-label">{k.replace(/_/g, ' ')}</div>
                <div className="stat-value">{pct(v)}</div>
              </div>
            ))}
          </div>
        </>
      )}

      {ctx.crop_area && (
        <>
          <h3 style={{ marginTop: 18 }}>Crop Area</h3>
          <div className="grid cols-4">
            <div className="stat"><div className="stat-label">Cultivated Area</div><div className="stat-value">{fmt(ctx.crop_area.total_cultivated_area)}</div></div>
            <div className="stat"><div className="stat-label">Irrigated Area</div><div className="stat-value">{fmt(ctx.crop_area.total_irrigated_area)}</div></div>
            <div className="stat"><div className="stat-label">Food Grain Area</div><div className="stat-value">{fmt(ctx.crop_area.food_grain_area)}</div></div>
            <div className="stat"><div className="stat-label">Food Grain Irrigated</div><div className="stat-value">{fmt(ctx.crop_area.food_grain_irrigated_area)}</div></div>
          </div>
        </>
      )}

      {ctx.crop_production && (
        <>
          <h3 style={{ marginTop: 18 }}>Crop Production</h3>
          <div className="grid cols-3">
            <div className="stat"><div className="stat-label">Cereals</div><div className="stat-value">{fmt(ctx.crop_production.cereals_all)}</div></div>
            <div className="stat"><div className="stat-label">Pulses</div><div className="stat-value">{fmt(ctx.crop_production.pulses_all)}</div></div>
            <div className="stat"><div className="stat-label">Total Production</div><div className="stat-value">{fmt(ctx.crop_production.total_production)}</div></div>
          </div>
        </>
      )}

      {ctx.dairy && (
        <>
          <h3 style={{ marginTop: 18 }}>Dairy Development (2010-11)</h3>
          <div className="grid cols-4">
            <div className="stat"><div className="stat-label">Coop Societies</div><div className="stat-value">{fmt(ctx.dairy.dairy_cooperative_societies)}</div></div>
            <div className="stat"><div className="stat-label">Members</div><div className="stat-value">{fmt(ctx.dairy.total_members)}</div></div>
            <div className="stat"><div className="stat-label">Daily Avg Milk (000 L)</div><div className="stat-value">{fmt(ctx.dairy.daily_average_000_litre)}</div></div>
            <div className="stat"><div className="stat-label">Cold Storages</div><div className="stat-value">{fmt(ctx.dairy.cold_storages)}</div></div>
          </div>
        </>
      )}

      {(!ctx.workforce && !ctx.occupation && !ctx.crop_area && !ctx.crop_production && !ctx.dairy) && (
        <p className="small">Data not available for this district.</p>
      )}
    </div>
  )
}
