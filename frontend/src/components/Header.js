import React, { Component } from 'react';
import '@fortawesome/fontawesome-free/css/all.min.css';
import '../styles/Header.css'

class Header extends Component {
  render() {
    return (
      <header className="header">
        <div className="header__title">
          <h1>Dashboard</h1>
          <p>Friday, 26 June 2020</p>
        </div>
        <div className="header__search">
          <input type="text" placeholder="Search here..." />
          <button type="button">
            <i className="fa fa-search"></i> {/* Icon search */}
          </button>
        </div>
      </header>
    );
  }
}

export default Header;
