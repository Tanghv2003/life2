import React, { Component } from 'react';
import './Profile.css';

class Profile extends Component {
  constructor(props) {
    super(props);
    // Giả lập dữ liệu người dùng
    this.state = {
      user: {
        name: 'Nguyễn Văn A',
        avatar: 'https://via.placeholder.com/150',
        age: 25,
        height: 175, // cm
        weight: 70 // kg
      }
    };
  }

  render() {
    const { name, avatar, age, height, weight } = this.state.user;

    return (
      <div className="profile-container">

        <div>
          <h1>My Profile</h1>
        </div>
        <div>
          <img src={avatar} alt="Avatar" className="profile-avatar" />
          <h2 className="profile-name">{name}</h2>
          <p>Tuổi: {age}</p>
          <p>Chiều cao: {height} cm</p>
          <p>Cân nặng: {weight} kg</p>
        </div>
        
      </div>
    );
  }
}

export default Profile;
