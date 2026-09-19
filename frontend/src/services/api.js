const BASE = 'http://127.0.0.1:8000'

async function j(method, url, body) {
  const opts = { method, headers: { 'Content-Type': 'application/json' } }
  if (body) opts.body = JSON.stringify(body)
  const res = await fetch(`${BASE}${url}`, opts)
  if (!res.ok) {
    let detail = `HTTP ${res.status}`
    try { const e = await res.json(); detail = e.detail || detail } catch {}
    throw new Error(detail)
  }
  return res.json()
}

export const api = {
  health: () => j('GET', '/health'),
  districts: () => j('GET', '/districts'),
  villages: (district) => j('GET', `/villages/${encodeURIComponent(district)}`),
  recommend: (body) => j('POST', '/recommend', body),
  financial: (body) => j('POST', '/financial-analysis', body),
  whatIf: (body) => j('POST', '/what-if', body),
  clusterProfile: () => j('GET', '/cluster-profile'),
}
