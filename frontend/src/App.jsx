import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import Header from './components/Header.jsx'
import Home from './pages/Home.jsx'
import Advisor from './pages/Advisor.jsx'
import Results from './pages/Results.jsx'
import Financial from './pages/Financial.jsx'
import Methodology from './pages/Methodology.jsx'

export default function App() {
  return (
    <>
      <Header />
      <div className="container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/advisor" element={<Advisor />} />
          <Route path="/results" element={<Results />} />
          <Route path="/financial" element={<Financial />} />
          <Route path="/methodology" element={<Methodology />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </>
  )
}
