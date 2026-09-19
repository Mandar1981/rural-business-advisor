import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../services/api.js'
import DistrictSelector from '../components/DistrictSelector.jsx'
import VillageSelector from '../components/VillageSelector.jsx'
import BudgetInput from '../components/BudgetInput.jsx'

export default function Advisor() {
  const nav = useNavigate()
  const [districts, setDistricts] = useState([])
  const [villages, setVillages] = useState([])
  const [district, setDistrict] = useState('')
  const [village, setVillage] = useState('')
  const [budget, setBudget] = useState('200000')
  const [name, setName] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    api.districts().then(r => setDistricts(r.districts)).catch(e => setError(e.message))
  }, [])

  useEffect(() => {
    setVillage(''); setVillages([])
    if (!district) return
    api.villages(district).then(r => setVillages(r.villages)).catch(e => setError(e.message))
  }, [district])

  const submit = async () => {
    setError('')
    if (!district || !village || !budget) {
      setError('Please select district, village and enter budget.')
      return
    }
    setLoading(true)
    try {
      const data = await api.recommend({ district, village, budget: Number(budget), name: name || null })
      sessionStorage.setItem('rba_result', JSON.stringify(data))
      sessionStorage.setItem('rba_inputs', JSON.stringify({ district, village, budget: Number(budget), name }))
      nav('/results')
    } catch (e) { setError(e.message) }
    finally { setLoading(false) }
  }

  return (
    <div className="card" style={{ maxWidth: 640, margin: '40px auto' }}>
      <h2>Find Business Opportunities</h2>
      <p className="small" style={{ marginTop: 0 }}>
        Enter District, Village and Budget. Everything else is derived automatically
        from the village dataset and district context - you do not enter ML features.
      </p>
      {error && <div className="error-banner">{error}</div>}
      <DistrictSelector districts={districts} value={district} onChange={setDistrict} />
      <VillageSelector villages={villages} value={village} onChange={setVillage} disabled={!district} />
      <BudgetInput value={budget} onChange={setBudget} />
      <div className="form-row">
        <label>Name (optional)</label>
        <input type="text" value={name} onChange={e => setName(e.target.value)} placeholder="Your name (optional)" />
      </div>
      <button className="btn" onClick={submit} disabled={loading}>
        {loading ? 'Analyzing village...' : 'FIND BUSINESS OPPORTUNITIES'}
      </button>
    </div>
  )
}
