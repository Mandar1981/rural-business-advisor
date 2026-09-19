import React from 'react'
import { Link } from 'react-router-dom'

export default function Home() {
  return (
    <>
      <div className="hero">
        <h1>Rural Business Advisor</h1>
        <p>
          A data-driven rural business decision-support platform for Maharashtra.
          Enter a district, village and budget - the system builds a digital profile,
          clusters the village, derives opportunity signals, ranks business options,
          checks budget fit, predicts a proxy category via Random Forest, and runs
          financial feasibility.
        </p>
        <div className="chain">
          <span>Village Data</span><span className="arrow">-&gt;</span>
          <span>Digital Profile</span><span className="arrow">-&gt;</span>
          <span>K-Means Cluster</span><span className="arrow">-&gt;</span>
          <span>Opportunity Signals</span><span className="arrow">-&gt;</span>
          <span>Business Options</span><span className="arrow">-&gt;</span>
          <span>Budget Fit</span><span className="arrow">-&gt;</span>
          <span>RF Proxy Prediction</span><span className="arrow">-&gt;</span>
          <span>Financial Simulation</span><span className="arrow">-&gt;</span>
          <span>Funding Gap</span><span className="arrow">-&gt;</span>
          <span>PMEGP</span>
        </div>
      </div>

      <div className="grid cols-3">
        <div className="card">
          <h3>Village Digital Profile</h3>
          <p className="small">
            Population, workers, cultivators, agri-labour, and the 12 amenity
            features are pulled automatically from the village dataset.
          </p>
        </div>
        <div className="card">
          <h3>Opportunity Signal Engine</h3>
          <p className="small">
            Transparent, rule-based signals derived from available indicators.
            Signals are not proof of market demand.
          </p>
        </div>
        <div className="card">
          <h3>Financial Feasibility</h3>
          <p className="small">
            Break-even, payback, ROI and a what-if simulator using your assumptions.
          </p>
        </div>
      </div>

      <div className="card">
        <h2>Why is this different?</h2>
        <p>
          We do <strong>not</strong> just recommend a business. We build a
          data-driven feasibility profile for a specific rural village, then
          filter and rank business categories through budget reality, opportunity
          signals and financial simulation.
        </p>
        <Link to="/advisor"><button className="btn">Find Business Opportunities</button></Link>
      </div>
    </>
  )
}
