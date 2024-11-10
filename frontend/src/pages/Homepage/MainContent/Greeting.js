import React, { Component } from 'react';
import '../MainContent/Greeting.css'
class Greeting extends Component {
  render() {
    const { name, imageUrl } = this.props;  // Lấy tên người dùng và URL hình ảnh từ props
    return (
      <div className="greeting-container">
        <div className="text">
          <h1>Hello, {name}!</h1>
          <a>Hãy uống đủ 2l nước mỗi ngày</a>
        </div>

        <div className="img">
          <img 
            src={imageUrl || "https://via.placeholder.com/150"}  
            alt={`${name}'s profile`} 
            className="profile-image"
          />
        </div>
      </div>
    );
  }
}

export default Greeting;
