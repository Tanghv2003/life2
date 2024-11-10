import { Module } from '@nestjs/common';
import { SensorModule } from './sensor/sensor.module';
import { AppController } from './app.controller';



@Module({
  imports: [SensorModule], // Đảm bảo SensorModule được import ở đây
})
export class AppModule {}
