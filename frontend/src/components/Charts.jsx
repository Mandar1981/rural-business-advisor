import React from 'react'
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid,
  LineChart, Line, Legend, RadarChart, PolarGrid, PolarAngleAxis, Radar,
} from 'recharts'

export function OpportunityScoresChart({ scores }) {
  if (!scores) return null
  const data = Object.entries(scores).map(([k, v]) => ({ name: k, value: +(v * 100).toFixed(2) }))
  return (
    <div className="card">
      <h2>Opportunity Score by Category</h2>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={data} layout="vertical" margin={{ left: 40, right: 20 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis type="number" domain={[0, 100]} />
          <YAxis type="category" dataKey="name" width={180} />
          <Tooltip formatter={(v) => `${v}`} />
          <Bar dataKey="value" fill="#2f8f5f" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

export function InfrastructureChart({ infrastructure }) {
  if (!infrastructure) return null
  const entries = Object.entries(infrastructure).filter(([, v]) => v !== null)
  if (!entries.length) return null
  const data = entries.map(([k, v]) => ({ name: k, value: v }))
  return (
    <div className="card">
      <h2>Village Infrastructure</h2>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} margin={{ left: 40, right: 20, bottom: 80 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" angle={-35} textAnchor="end" interval={0} height={100} />
          <YAxis />
          <Tooltip />
          <Bar dataKey="value" fill="#1f6b45" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

export function FinancialProfitChart({ financial }) {
  if (!financial) return null
  const data = [
    { name: 'Revenue', value: financial.monthly_revenue },
    { name: 'Total Cost', value: financial.total_monthly_cost },
    { name: 'Profit', value: financial.monthly_profit },
  ]
  return (
    <div className="card">
      <h2>Monthly Financial Snapshot</h2>
      <ResponsiveContainer width="100%" height={260}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="value" fill="#c47a00" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

export function BreakEvenChart({ sellingPrice, variableCost, fixedCost, breakEvenQty }) {
  if (sellingPrice == null) return null
  const maxQ = Math.max(breakEvenQty ? breakEvenQty * 2 : 100, 100)
  const step = Math.max(1, Math.floor(maxQ / 20))
  const data = []
  for (let q = 0; q <= maxQ; q += step) {
    data.push({ qty: q, cost: fixedCost + variableCost * q, revenue: sellingPrice * q })
  }
  return (
    <div className="card">
      <h2>Break-even Chart</h2>
      <ResponsiveContainer width="100%" height={280}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="qty" label={{ value: 'Quantity', position: 'insideBottom', offset: -4 }} />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="cost" stroke="#b23b3b" name="Total Cost" dot={false} />
          <Line type="monotone" dataKey="revenue" stroke="#2f8f5f" name="Revenue" dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

export function ClusterRadarChart({ profiles }) {
  if (!profiles?.length) return null
  const features = Object.keys(profiles[0].means).slice(0, 8)
  const data = features.map(f => {
    const row = { feature: f.length > 22 ? f.slice(0, 22) + '...' : f }
    profiles.forEach(p => { row[`Cluster ${p.cluster_id}`] = p.means[f] })
    return row
  })
  const colors = ['#2f8f5f', '#c47a00', '#2e5aac', '#b23b3b', '#6a4fb2', '#1f6b45']
  return (
    <div className="card">
      <h2>Cluster Profiles (Feature Averages)</h2>
      <ResponsiveContainer width="100%" height={340}>
        <RadarChart data={data}>
          <PolarGrid />
          <PolarAngleAxis dataKey="feature" />
          {profiles.map((p, i) => (
            <Radar key={p.cluster_id} name={`Cluster ${p.cluster_id}`}
              dataKey={`Cluster ${p.cluster_id}`}
              stroke={colors[i % colors.length]} fill={colors[i % colors.length]} fillOpacity={0.15} />
          ))}
          <Legend />
          <Tooltip />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  )
}
