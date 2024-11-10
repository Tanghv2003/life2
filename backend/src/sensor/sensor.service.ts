import { Injectable } from '@nestjs/common';

@Injectable()
export class SensorService {
  // Giả sử dữ liệu cảm biến là cố định
  getSensorData() {
    const sensorData = {
      temperature: 24.5, // Nhiệt độ
      heartRate: 75, // Nhịp tim
      acceleration: 0.98, // Gia tốc
    };

    return sensorData;
  }
}
