import { Controller, Get } from '@nestjs/common';
import { SensorService } from './sensor/sensor.service';


@Controller('sensor')  // Kiểm tra route của controller
export class AppController {
  constructor(private readonly sensorService: SensorService) {}

  @Get()
  getSensorData() {
    return this.sensorService.getSensorData();  // Trả về dữ liệu từ service
  }
}
