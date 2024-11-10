// src/App.js
import React, { Component } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Homepage/Home';
import './App.css'
import HistoryPage from './pages/HistoryPage/HistoryPage';


class App extends Component {
  render() {
    return (
      <Router>
        <div className='app'>
          {/* Navbar */}
          <Navbar />

          {/* Các tuyến đường */}
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="history" element={<HistoryPage />} />
            <Route path="about" element = {<Home/>}/>
          </Routes>
        </div>
      </Router>
    );
  }
}

export default App;
