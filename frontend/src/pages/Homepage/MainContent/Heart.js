// Heart.js
import React, { Component } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, LineElement, CategoryScale, LinearScale, PointElement } from 'chart.js';

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement);

class Heart extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: {
        labels: [],
        datasets: [
          {
            label: 'Nhịp tim',
            data: [],
            borderColor: 'rgb(255, 99, 132)',
            backgroundColor: 'rgba(255, 99, 132, 0.5)',
            borderWidth: 2,
          },
        ],
      },
      options: {
        maintainAspectRatio: false, // Tắt giữ tỷ lệ
      },
    };
  }

  componentDidMount() {
    this.intervalId = setInterval(this.updateData, 1000);
  }

  componentWillUnmount() {
    clearInterval(this.intervalId);
  }

  updateData = () => {
    const randomHeartRate = Math.floor(Math.random() * (100 - 60 + 1)) + 60;

    this.setState((prevState) => {
      const newLabels = [...prevState.data.labels, new Date().toLocaleTimeString()];
      const newData = [...prevState.data.datasets[0].data, randomHeartRate];

      if (newLabels.length > 20) {
        newLabels.shift();
        newData.shift();
      }

      return {
        data: {
          ...prevState.data,
          labels: newLabels,
          datasets: [
            {
              ...prevState.data.datasets[0],
              data: newData,
            },
          ],
        },
      };
    });
  };

  render() {
    return (
      <div style={{ width: 1100, height: 400 }}>
        <h2>Biểu đồ nhịp tim</h2>
        <Line data={this.state.data} options={this.state.options} />
      </div>
    );
  }
}

export default Heart;
