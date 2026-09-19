import React, { useMemo, useState } from 'react'

export default function VillageSelector({ villages, value, onChange, disabled }) {
  const [query, setQuery] = useState('')
  const filtered = useMemo(() => {
    const q = query.toLowerCase()
    return villages.filter(v => v.toLowerCase().includes(q))
  }, [villages, query])

  return (
    <div className="form-row">
      <label>Village</label>
      <input type="text"
        placeholder={disabled ? 'Select a district first' : 'Search village...'}
        value={query} onChange={e => setQuery(e.target.value)} disabled={disabled} />
      <select value={value} onChange={e => onChange(e.target.value)}
        disabled={disabled} style={{ marginTop: 8 }}>
        <option value="">Select village</option>
        {filtered.map(v => <option key={v} value={v}>{v}</option>)}
      </select>
      {!disabled && <span className="small" style={{ marginTop: 4 }}>{filtered.length} villages</span>}
    </div>
  )
}
