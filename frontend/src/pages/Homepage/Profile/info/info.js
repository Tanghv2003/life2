// Info.js
import React from 'react';
import editIcon from '../../../../assets/edit.png';
import docIcon from '../../../../assets/doc.png';
import './info.css';

// Hàm để định dạng ngày sinh chỉ bao gồm ngày, tháng và năm
const formatDateOfBirth = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { // Sử dụng tiếng Anh
    year: 'numeric', month: 'long', day: 'numeric' // Chỉ lấy ngày, tháng, năm
  });
};

class Info extends React.Component {
  render() {
    // Thông tin người dùng mặc định
    const user = {
      name: 'Nguyễn Văn A',
      avatar: 'https://example.com/avatar.png',
      dateOfBirth: '1998-12-15',
      height: 170,
      weight: 65,
      gender: 'Male',  // Giới tính bằng tiếng Anh
    };

    return (
      <div className="user-info">
        {/* Phần tiêu đề và nút edit */}
        <div className="header1a">
          <h2>My Profile</h2>

          <div>
          <button className="edit-btn">
            <img src={editIcon} alt="Edit" />
          </button>

          <button className="edit-btn">
            <img src={docIcon} alt="Edit" />
          </button>
          </div>
          
        </div>

        {/* Phần avatar và thông tin người dùng */}
        <div className="user-info-content">
          <img src={user.avatar} alt="Avatar" className="avatar" />
          <div className="user-details">
            <p><strong>Name:</strong> {user.name}</p> {/* Sửa "Tên" thành "Name" */}
            <p><strong>Date of Birth:</strong> {formatDateOfBirth(user.dateOfBirth)}</p> {/* Ngày sinh chỉ hiển thị ngày, tháng, năm */}
          </div>
        </div>

        {/* Thông tin chiều cao, cân nặng và giới tính nằm ngang hàng */}
        <div className="user-stats">
          <p><strong>Height:</strong><span className="stat-value">{user.height} cm</span></p> {/* Sửa "Chiều cao" thành "Height" */}
          <p><strong>Weight:</strong><span className="stat-value">{user.weight} kg</span></p> {/* Sửa "Cân nặng" thành "Weight" */}
          <p><strong>Gender:</strong><span className="stat-value">{user.gender}</span></p> {/* Sửa "Giới tính" thành "Gender" */}
        </div>
      </div>
    );
  }
}

export default Info;
