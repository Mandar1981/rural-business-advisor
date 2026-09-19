import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import VillageProfile from '../components/VillageProfile.jsx'
import ClusterCard from '../components/ClusterCard.jsx'
import OpportunitySignals from '../components/OpportunitySignals.jsx'
import BusinessRecommendation from '../components/BusinessRecommendation.jsx'
import MLResult from '../components/MLResult.jsx'
import EconomicContext from '../components/EconomicContext.jsx'
import PMEGPCard from '../components/PMEGPCard.jsx'
import { OpportunityScoresChart, InfrastructureChart, ClusterRadarChart } from '../components/Charts.jsx'

export default function Results() {
  const [data, setData] = useState(null)
  const [inputs, setInputs] = useState(null)

  useEffect(() => {
    const raw = sessionStorage.getItem('rba_result')
    const inp = sessionStorage.getItem('rba_inputs')
    if (raw) setData(JSON.parse(raw))
    if (inp) setInputs(JSON.parse(inp))
  }, [])

  if (!data) {
    return (
      <div className="card">
        <h2>No results yet</h2>
        <p>Please run the advisor first.</p>
        <Link to="/advisor"><button className="btn">Go to Advisor</button></Link>
      </div>
    )
  }

  return (
    <>
      <div className="card">
        <h2>Rural Business Advisor - Result Dashboard</h2>
        <div className="grid cols-3">
          <div className="stat"><div className="stat-label">District</div><div className="stat-value">{inputs?.district}</div></div>
          <div className="stat"><div className="stat-label">Village</div><div className="stat-value" style={{ fontSize: 16 }}>{inputs?.village}</div></div>
          <div className="stat"><div className="stat-label">Available Budget</div><div className="stat-value">Rs. {Number(inputs?.budget).toLocaleString()}</div></div>
        </div>
        {inputs?.name && <p className="small" style={{ marginTop: 10 }}>Prepared for: <strong>{inputs.name}</strong></p>}
      </div>

      <VillageProfile village={data.village} />
      <InfrastructureChart infrastructure={data.infrastructure} />
      <ClusterCard cluster={data.cluster} />
      <ClusterRadarChart profiles={[data.cluster?.cluster_profile].filter(Boolean)} />

      <OpportunitySignals signals={data.opportunity_signals} />
      <OpportunityScoresChart scores={data.opportunity_scores} />
      <BusinessRecommendation recommendations={data.business_recommendations} />
      <MLResult ml={data.ml_prediction} />
      <EconomicContext ctx={data.economic_context} />

      <div className="card">
        <h2>Funding Gap</h2>
        <div className="grid cols-3">
          <div className="stat"><div className="stat-label">Top Recommendation - Required</div><div className="stat-value">Rs. {Number(data.budget_analysis.top_recommendation_required_investment).toLocaleString()}</div></div>
          <div className="stat"><div className="stat-label">Your Capital</div><div className="stat-value">Rs. {Number(data.budget_analysis.user_budget).toLocaleString()}</div></div>
          <div className="stat"><div className="stat-label">Funding Gap</div><div className="stat-value">Rs. {Number(data.budget_analysis.funding_gap).toLocaleString()}</div></div>
        </div>
      </div>

      <PMEGPCard pmegp={data.pmegp} />

      <div className="card">
        <h2>Why this recommendation?</h2>
        <p>
          The selected village profile shows <strong>{data.village.village}</strong> in {data.village.district}.
          The K-Means model placed it in cluster <strong>{data.cluster.cluster_id}</strong>.
          The opportunity engine surfaced <strong>{data.opportunity_signals.length}</strong> signal(s).
          The top category is <strong>{data.business_recommendations[0]?.business_category}</strong> with an
          opportunity score of <strong>{((data.business_recommendations[0]?.opportunity_score || 0) * 100).toFixed(1)}</strong>.
          Budget fit: <strong>{data.business_recommendations[0]?.budget_fit}</strong>.
        </p>
      </div>

      <div className="card">
        <h2>Limitations</h2>
        <ul>{data.limitations?.map((l, i) => <li key={i}>{l}</li>)}</ul>
      </div>
    </>
  )
}
