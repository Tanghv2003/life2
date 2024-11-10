// src/pages/HistoryPage.js

import React, { Component } from 'react';
import { getdata } from '../../services/getdata';

class HistoryPage extends Component {
  state = {
    sensorData: {},  // Dữ liệu sensor (đối tượng)
  };

  async componentDidMount() {
    try {
      const data = await getdata();  // Lấy dữ liệu từ API
      this.setState({ sensorData: data });
    } catch (error) {
      console.error('Không thể lấy dữ liệu:', error);
    }
  }

  render() {
    const { sensorData } = this.state;

    return (
      <div>
        <h1>Lịch sử cảm biến</h1>
        <div>
          <strong>Thời gian: {new Date().toLocaleString()}</strong>
        </div>
        <div>
          {/* Kiểm tra nếu sensorData có giá trị và hiển thị thông tin */}
          {sensorData ? (
            <div>
              <p>Nhiệt độ: {sensorData.temperature}°C</p>
              <p>Nhịp tim: {sensorData.heartRate} bpm</p>
              <p>Gia tốc: {sensorData.acceleration} m/s²</p>
            </div>
          ) : (
            <p>Không có dữ liệu để hiển thị</p>  // Trường hợp không có dữ liệu
          )}
        </div>
      </div>
    );
  }
}

export default HistoryPage;
