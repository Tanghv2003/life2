import React, { useState } from 'react';
import './check.css';

// Lưu lịch sử khảo sát trong localStorage hoặc có thể thay thế bằng API
const loadHistory = () => {
  const history = JSON.parse(localStorage.getItem('surveyHistory')) || [];
  return history;
};

const saveSurvey = (surveyData) => {
  let history = loadHistory();

  // Kiểm tra xem ngày đã tồn tại chưa
  const existingIndex = history.findIndex(survey => survey.date === surveyData.date);
  if (existingIndex !== -1) {
    // Nếu tồn tại, cập nhật thông tin
    history[existingIndex] = surveyData;
  } else {
    // Nếu không tồn tại, thêm mới
    history.push(surveyData);
  }

  localStorage.setItem('surveyHistory', JSON.stringify(history));
};

const Check = () => {
  const [date, setDate] = useState('');
  const [physicalHealth, setPhysicalHealth] = useState('');
  const [mentalHealth, setMentalHealth] = useState('');
  const [history, setHistory] = useState(loadHistory());
  const [filteredHistory, setFilteredHistory] = useState(history);

  const handleSubmit = (e) => {
    e.preventDefault();

    // Lưu thông tin khảo sát vào lịch sử
    const surveyData = {
      date: date,
      physicalHealth: physicalHealth,
      mentalHealth: mentalHealth,
    };

    saveSurvey(surveyData);
    setHistory(loadHistory()); // Cập nhật lại lịch sử

    // Reset form
    setDate('');
    setPhysicalHealth('');
    setMentalHealth('');
  };

  const handleDateChange = (e) => {
    const selectedDate = e.target.value;
    setDate(selectedDate);

    // Lọc lịch sử theo ngày được chọn
    const filtered = history.filter(survey => survey.date === selectedDate);
    setFilteredHistory(filtered);
  };

  return (
    <div className="survey-container">
      <header className="survey-header">
        <h1 className="survey-title">Daily Check</h1>
      </header>

      <form className="survey-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="form-label">Date: </label>
          <input
            type="date"
            className="form-input"
            value={date}
            onChange={handleDateChange}
            required
          />
        </div>
        <div className="form-group">
          <label className="form-label">Physical Health: </label>
          <select
            className="form-select"
            value={physicalHealth}
            onChange={(e) => setPhysicalHealth(e.target.value)}
            required
          >
            <option value="">Select level</option>
            <option value="Very Bad">Very Bad</option>
            <option value="Bad">Bad</option>
            <option value="Normal">Normal</option>
            <option value="Good">Good</option>
            <option value="Very Good">Very Good</option>
          </select>
        </div>
        <div className="form-group">
          <label className="form-label">Mental Health: </label>
          <select
            className="form-select"
            value={mentalHealth}
            onChange={(e) => setMentalHealth(e.target.value)}
            required
          >
            <option value="">Select level</option>
            <option value="Very Bad">Very Bad</option>
            <option value="Bad">Bad</option>
            <option value="Normal">Normal</option>
            <option value="Good">Good</option>
            <option value="Very Good">Very Good</option>
          </select>
        </div>
        <button type="submit" className="form-button">Save Survey</button>
      </form>

      <h3 className="history-title">Survey History</h3>
      {date ? (
        filteredHistory.length > 0 ? (
          <ul className="history-list">
            {filteredHistory.map((survey, index) => (
              <li key={index} className="history-item">
                <strong>{survey.date}</strong>: Physical {survey.physicalHealth}, Mental {survey.mentalHealth}
              </li>
            ))}
          </ul>
        ) : (
          <p className="history-empty">No data available for this date.</p>
        )
      ) : (
        <p className="history-empty">Please select a date to view the history.</p>
      )}
    </div>
  );
};

export default Check;
