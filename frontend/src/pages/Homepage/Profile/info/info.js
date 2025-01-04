import React, { useState } from 'react';
import editIcon from '../../../../assets/edit.png';
import docIcon from '../../../../assets/doc.png';
import './info.css';

const formatDateOfBirth = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

const Info = () => {
  // State cho thông tin người dùng
  const [user, setUser] = useState({
    name: 'Nguyễn Văn A',
    avatar: 'https://example.com/avatar.png',
    dateOfBirth: '1998-12-15',
    height: 170,
    weight: 65,
    gender: 'Male',
  });

  // State để điều khiển hiển thị modal
  const [isEditOpen, setIsEditOpen] = useState(false);
  
  // State cho giá trị đang chỉnh sửa
  const [editValues, setEditValues] = useState({...user});

  // Xử lý mở modal chỉnh sửa
  const handleEditClick = () => {
    setEditValues({...user});
    setIsEditOpen(true);
  };

  // Xử lý lưu thay đổi
  const handleSave = () => {
    setUser({...editValues});
    setIsEditOpen(false);
  };

  // Xử lý thay đổi input
  const handleInputChange = (field, value) => {
    setEditValues(prev => ({
      ...prev,
      [field]: value
    }));
  };

  return (
    <div className="user-info">
      <div className="header1a">
        <h2>My Profile</h2>
        <div>
          <button className="edit-btn" onClick={handleEditClick}>
            <img src={editIcon} alt="Edit" />
          </button>
          <button className="edit-btn">
            <img src={docIcon} alt="Edit" />
          </button>
        </div>
      </div>

      <div className="user-info-content">
        <img src={user.avatar} alt="Avatar" className="avatar" />
        <div className="user-details">
          <p><strong>Name:</strong> {user.name}</p>
          <p><strong>Date of Birth:</strong> {formatDateOfBirth(user.dateOfBirth)}</p>
        </div>
      </div>

      <div className="user-stats">
        <p><strong>Height:</strong><span className="stat-value">{user.height} cm</span></p>
        <p><strong>Weight:</strong><span className="stat-value">{user.weight} kg</span></p>
        <p><strong>Sex:</strong><span className="stat-value">{user.gender}</span></p>
      </div>

      {/* Modal chỉnh sửa */}
      {isEditOpen && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h2>UPDATE INFOMATION</h2>
            
            <div className="form-group">
              <label>Name:</label>
              <input
                type="text"
                value={editValues.name}
                onChange={(e) => handleInputChange('name', e.target.value)}
              />
            </div>
            
            <div className="form-group">
              <label>Date of Birth:</label>
              <input
                type="date"
                value={editValues.dateOfBirth}
                onChange={(e) => handleInputChange('dateOfBirth', e.target.value)}
              />
            </div>
            
            <div className="form-group">
              <label>Height: (cm):</label>
              <input
                type="number"
                value={editValues.height}
                onChange={(e) => handleInputChange('height', parseInt(e.target.value))}
              />
            </div>
            
            <div className="form-group">
              <label> Weight (kg):</label>
              <input
                type="number"
                value={editValues.weight}
                onChange={(e) => handleInputChange('weight', parseInt(e.target.value))}
              />
            </div>
            
            <div className="form-group">
              <label>Sex:</label>
              <select
                value={editValues.gender}
                onChange={(e) => handleInputChange('gender', e.target.value)}
              >
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
            </div>

            <div className="modal-buttons">
              <button className="btn-cancel" onClick={() => setIsEditOpen(false)}>
                Cancel
              </button>
              <button className="btn-save" onClick={handleSave}>
                Save
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Info;