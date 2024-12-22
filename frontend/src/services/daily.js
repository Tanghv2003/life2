import axios from 'axios';

// URL backend của bạn
const BASE_URL = 'http://localhost:3001/daily-check';

// API để lấy tất cả dữ liệu DailyCheck
export const getAllDailyChecks = async () => {
  try {
    const response = await axios.get(BASE_URL);  // Gửi yêu cầu GET để lấy tất cả dữ liệu
    return response.data;  // Trả về dữ liệu của DailyCheck
  } catch (error) {
    console.error('Không thể lấy danh sách DailyChecks', error);
    throw error;  // Ném lỗi nếu có vấn đề khi lấy dữ liệu
  }
};

// API để thêm một bản ghi DailyCheck
export const createDailyCheck = async (physicalHealth, mentalHealth) => {
  try {
    const response = await axios.post(BASE_URL, {
      physicalHealth,
      mentalHealth,
      timestamp: new Date().toISOString(),  // Thêm timestamp vào dữ liệu
    });
    return response.data;  // Trả về bản ghi vừa thêm
  } catch (error) {
    console.error('Không thể thêm DailyCheck', error);
    throw error;  // Ném lỗi nếu có vấn đề khi thêm dữ liệu
  }
};

// API để cập nhật một bản ghi DailyCheck
export const updateDailyCheck = async (id, physicalHealth, mentalHealth) => {
  try {
    const response = await axios.put(`${BASE_URL}/${id}`, {
      physicalHealth,
      mentalHealth,
      timestamp: new Date().toISOString(),  // Thêm timestamp vào dữ liệu
    });
    return response.data;  // Trả về bản ghi đã cập nhật
  } catch (error) {
    console.error('Không thể cập nhật DailyCheck', error);
    throw error;  // Ném lỗi nếu có vấn đề khi cập nhật dữ liệu
  }
};
