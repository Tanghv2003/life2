import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale } from 'chart.js';
import './InsightPage.css';  // Import CSS
import { getdata } from '../../services/getdata';

// Đăng ký các thành phần Chart.js
ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale);

const InsightsPage = () => {
    const [sensorData, setSensorData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await getdata();  // Giả sử getdata() là hàm gọi API
                setSensorData(data);  // Lưu dữ liệu nhận được vào state
            } catch (error) {
                console.error('Không thể lấy dữ liệu:', error);
            }
        };

        fetchData();
    }, []);

    // Dữ liệu cho biểu đồ với 4 đường
    const chartData = {
        labels: sensorData.map(item => new Date(item.timestamp).toLocaleTimeString()), // Mảng thời gian từ timestamp
        datasets: [
            {
                label: 'Nhịp Tim (bpm)', // Đường nhịp tim
                data: sensorData.map(item => item.heartRate), // Lấy dữ liệu nhịp tim
                fill: false,
                borderColor: 'rgb(75, 192, 192)', // Màu sắc cho đường nhịp tim
                tension: 0.1,
            },
            {
                label: 'Nhiệt Độ (°C)', // Đường nhiệt độ
                data: sensorData.map(item => item.temperature), // Lấy dữ liệu nhiệt độ
                fill: false,
                borderColor: 'rgb(255, 99, 132)', // Màu sắc cho đường nhiệt độ
                tension: 0.1,
            },
            {
                label: 'Độ Ẩm (%)', // Đường độ ẩm
                data: sensorData.map(item => item.humidity), // Lấy dữ liệu độ ẩm
                fill: false,
                borderColor: 'rgb(54, 162, 235)', // Màu sắc cho đường độ ẩm
                tension: 0.1,
            },
            {
                label: 'Gia Tốc (m/s²)', // Đường gia tốc
                data: sensorData.map(item => Math.sqrt(item.acceleration.x ** 2 + item.acceleration.y ** 2 + item.acceleration.z ** 2)), // Tính gia tốc tổng hợp
                fill: false,
                borderColor: 'rgb(153, 102, 255)', // Màu sắc cho đường gia tốc
                tension: 0.1,
            },
        ],
    };

    const options = {
        responsive: true,
        plugins: {
            title: {
                display: true,
                text: 'Biểu Đồ Nhịp Tim, Nhiệt Độ, Độ Ẩm và Gia Tốc',
            },
            tooltip: {
                mode: 'index',
                intersect: false,
            },
        },
        scales: {
            x: {
                beginAtZero: true,
            },
            y: {
                beginAtZero: true,
            },
        },
    };

    return (
        <div className="insights-page">
            <h1>Health Insights</h1>
            {sensorData.length > 0 ? (
                <section>
                    <h2>Biểu Đồ Nhịp Tim, Nhiệt Độ, Độ Ẩm và Gia Tốc</h2>
                    <Line data={chartData} options={options} />
                </section>
            ) : (
                <p className="loading-message">Đang tải dữ liệu...</p>
            )}
        </div>
    );
};

export default InsightsPage;
