import React, { useState, useEffect } from 'react';
import './check.css';
import { getAllDailyChecks, updateDailyCheck, createDailyCheck } from '../../../../services/daily';

// Hàm chuyển đổi mức độ sức khỏe thành chuỗi "0" hoặc "1"
const convertHealthStatus = (healthStatus) => {
  return healthStatus === 'Good' ? '1' : '0';
};

const Check = () => {
  const [date, setDate] = useState('');
  const [physicalHealth, setPhysicalHealth] = useState('');
  const [mentalHealth, setMentalHealth] = useState('');
  const [surveyToEdit, setSurveyToEdit] = useState(null);
  const [notification, setNotification] = useState(null);

  // Lấy tất cả dữ liệu từ backend khi component được load
  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await getAllDailyChecks();
        const surveyForDate = data.find(survey => survey.date === date);  // Tìm bản ghi theo ngày
        if (surveyForDate) {
          setSurveyToEdit(surveyForDate);
          setPhysicalHealth(surveyForDate.physicalHealth === '1' ? 'Good' : 'Bad');
          setMentalHealth(surveyForDate.mentalHealth === '1' ? 'Good' : 'Bad');
        }
      } catch (error) {
        console.error('Không thể lấy dữ liệu Daily Check', error);
      }
    };

    if (date) fetchData();
  }, [date]);

  // Cập nhật hoặc tạo mới thông tin khảo sát
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const physicalHealthValue = convertHealthStatus(physicalHealth);
      const mentalHealthValue = convertHealthStatus(mentalHealth);

      const surveyData = {
        date: date,  // Giữ nguyên giá trị date, không thay đổi
        physicalHealth: physicalHealthValue,  // Chuyển thành chuỗi "0" hoặc "1"
        mentalHealth: mentalHealthValue,      // Chuyển thành chuỗi "0" hoặc "1"
      };

      if (surveyToEdit) {
        // Cập nhật bản ghi đã sửa
        const updatedSurvey = await updateDailyCheck(surveyToEdit.id, surveyData);
        setSurveyToEdit(updatedSurvey);  // Cập nhật bản ghi đã sửa
        setNotification({ type: 'success', message: 'Cập nhật thông tin khảo sát thành công!' });
      } else {
        // Tạo mới thông tin khảo sát
        const newSurvey = await createDailyCheck(surveyData);
        setSurveyToEdit(newSurvey);  // Cập nhật survey mới
        setNotification({ type: 'success', message: 'Tạo mới thông tin khảo sát thành công!' });
      }

      // Reset form sau khi lưu
      setPhysicalHealth('');
      setMentalHealth('');
    } catch (error) {
      console.error('Không thể lưu thông tin khảo sát', error);
      setNotification({ type: 'error', message: 'Có lỗi xảy ra, không thể lưu thông tin khảo sát!' });
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

      {/* Hiển thị thông báo nếu có */}
      {notification && (
        <div className={`notification ${notification.type}`}>
          {notification.message}
        </div>
      )}
    </div>
  );
};

export default Check;
