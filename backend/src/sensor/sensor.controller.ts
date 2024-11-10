import { Controller, Get } from '@nestjs/common';
import { SensorService } from './sensor.service';

@Controller('sensor') // Định nghĩa route chính cho cảm biến
export class SensorController {
  constructor(private readonly sensorService: SensorService) {}

  @Get() // Xử lý GET request tại route /sensor
  getSensorData() {
    // Gọi service để lấy dữ liệu cảm biến
    return this.sensorService.getSensorData();
  }
}
