import React from 'react'

export default function DistrictSelector({ districts, value, onChange }) {
  return (
    <div className="form-row">
      <label>District</label>
      <select value={value} onChange={e => onChange(e.target.value)}>
        <option value="">Select district</option>
        {districts.map(d => <option key={d} value={d}>{d}</option>)}
      </select>
    </div>
  )
}
