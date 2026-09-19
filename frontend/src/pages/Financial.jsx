import React, { useState } from 'react'
import FinancialSimulator from '../components/FinancialSimulator.jsx'
import WhatIfAnalysis from '../components/WhatIfAnalysis.jsx'
import { FinancialProfitChart, BreakEvenChart } from '../components/Charts.jsx'

export default function Financial() {
  const [result, setResult] = useState(null)
  const [form, setForm] = useState(null)

  return (
    <>
      <FinancialSimulator onResult={(r, f) => { setResult(r); setForm(f) }} />
      {result && form && (
        <>
          <FinancialProfitChart financial={result} />
          <BreakEvenChart
            sellingPrice={Number(form.selling_price_per_unit)}
            variableCost={Number(form.variable_cost_per_unit)}
            fixedCost={Number(form.monthly_fixed_cost)}
            breakEvenQty={result.break_even_quantity}
          />
        </>
      )}
      {form && <WhatIfAnalysis initialForm={form} />}
    </>
  )
}
