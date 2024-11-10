import { Module } from '@nestjs/common';
import { SensorController } from './sensor.controller';
import { SensorService } from './sensor.service';

@Module({
  controllers: [SensorController],
  providers: [SensorService], // Nếu bạn có service xử lý logic liên quan đến cảm biến
})
export class SensorModule {}
