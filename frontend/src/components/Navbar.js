// src/components/Navbar.js
import React, { Component } from 'react';
import { NavLink } from 'react-router-dom';
import   '../styles/Navbar.css'


class Navbar extends Component {
  render() {
    return (
      <nav className="navbar">
        <ul className="navbar-list">

          <li className="navbar-item">
            <NavLink to="/" exact activeClassName="active" className="navbar-link">
              Home
            </NavLink>
          </li>

          <li className="navbar-item">
            <NavLink to="/history" activeClassName="active" className="navbar-link">
              History
            </NavLink>
          </li>

          <li className="navbar-item">
            <NavLink to="/insights" activeClassName="active" className="navbar-link">
              Insights
            </NavLink>
          </li>

          <li className="navbar-item">
            <NavLink to="/advice" activeClassName="active" className="navbar-link">
              Advice
            </NavLink>
          </li>

          <li className="navbar-item">
            <NavLink to="/logout" activeClassName="active" className="navbar-link">
              Log out
            </NavLink>
          </li>



        </ul>
      </nav>
    );
  }
}

export default Navbar;
