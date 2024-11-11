import { Module } from '@nestjs/common';
import { SensorModule } from './sensor/sensor.module';
import { AppController } from './app.controller';
import { MqttModule } from './mqtt/mqtt.module';


@Module({
  imports: [SensorModule,MqttModule], // Đảm bảo SensorModule được import ở đây
})
export class AppModule {}