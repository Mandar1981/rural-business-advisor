import React from 'react'

export default function ClusterCard({ cluster }) {
  if (!cluster) return null
  const profile = cluster.cluster_profile || {}
  return (
    <div className="card">
      <h2>K-Means Village Cluster</h2>
      <div className="grid cols-3">
        <div className="stat"><div className="stat-label">Cluster ID</div><div className="stat-value">{cluster.cluster_id}</div></div>
        <div className="stat"><div className="stat-label">Cluster Size</div><div className="stat-value">{cluster.size ?? '-'}</div></div>
        <div className="stat"><div className="stat-label">Silhouette Score</div><div className="stat-value">{cluster.silhouette}</div></div>
      </div>
      {profile.description && <p style={{ marginTop: 14, lineHeight: 1.5 }}>{profile.description}</p>}
      {profile.strongest_features?.length > 0 && (
        <>
          <h3 style={{ marginTop: 14 }}>Strongest Amenity Signals in Cluster</h3>
          <ul>{profile.strongest_features.map((f, i) => <li key={i}>{f.feature} - mean {f.value}</li>)}</ul>
        </>
      )}
    </div>
  )
}
