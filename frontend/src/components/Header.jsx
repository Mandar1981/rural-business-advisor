import React from 'react'
import { NavLink } from 'react-router-dom'

export default function Header() {
  return (
    <header className="header">
      <h1>Rural Business Advisor</h1>
      <nav>
        <NavLink to="/" end>Home</NavLink>
        <NavLink to="/advisor">Advisor</NavLink>
        <NavLink to="/financial">Financial</NavLink>
        <NavLink to="/methodology">Methodology</NavLink>
      </nav>
    </header>
  )
}
