import React, { useState } from 'react';
import './check.css';
import { createDailyCheck } from '../../../../services/daily';

const Check = () => {
  const [date, setDate] = useState('');
  const [physicalHealth, setPhysicalHealth] = useState('');
  const [mentalHealth, setMentalHealth] = useState('');

  // Hàm chuyển đổi từ Good/Bad sang "1"/"0"
  const convertHealthStatus = (status) => {
    return status === 'Good' ? 1 : 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      // Tạo object data theo cấu trúc API yêu cầu
      const dailyCheckData = {
        physicalHealth: convertHealthStatus(physicalHealth),
        mentalHealth: convertHealthStatus(mentalHealth),
        timestamp: date
      };

      // Gọi API tạo bản ghi mới
      const response = await createDailyCheck(dailyCheckData);
      console.log('Đã tạo bản ghi thành công:', response);

      // Reset form
      setDate('');
      setPhysicalHealth('');
      setMentalHealth('');

      // Có thể thêm thông báo thành công ở đây
      alert('Đã lưu thông tin khảo sát!');
      
    } catch (error) {
      console.error('Không thể tạo bản ghi:', error);
      // Thông báo lỗi cho người dùng
      alert('Có lỗi xảy ra khi lưu thông tin!');
    }
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
            onChange={(e) => setDate(e.target.value)}
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
            <option value="Bad">Bad</option>
            <option value="Good">Good</option>
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
            <option value="Bad">Bad</option>
            <option value="Good">Good</option>
          </select>
        </div>
        <button type="submit" className="form-button">Save Survey</button>
      </form>
    </div>
  );
};

export default Check;