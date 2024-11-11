import { Controller, Logger, Post, Body, Inject } from '@nestjs/common';
import { ClientMqtt, MqttContext, Payload, MessagePattern, Ctx } from '@nestjs/microservices';
import { promises as fs } from 'fs';  // Để sử dụng fs promises
import * as path from 'path';
import { lastValueFrom } from 'rxjs';
import { PublishMessageDto } from './dto/public.dto';

@Controller('mqtt')
export class MqttController {
  private readonly logger = new Logger(MqttController.name);

  constructor(
    @Inject('MQTT_CLIENT') private readonly client: ClientMqtt,
  ) {}

  @Post('publish')
  async publishMessage(@Body() publishMessageDto: PublishMessageDto) {
    try {
      await lastValueFrom(
        this.client.emit(publishMessageDto.topic, publishMessageDto.message)
      );
    } catch (error) {
      this.logger.error('Failed to publish message', error);
      throw error;
    }
  }

  @MessagePattern('tanghv_topic')
  async getNotifications(@Payload() data: any, @Ctx() context: MqttContext) {
    this.logger.log(`Received message from topic ${context.getTopic()}: ${JSON.stringify(data)}`);
    console.log(`Received message from topic ${context.getTopic()}: ${JSON.stringify(data)}`);

    // Thêm thời gian nhận dữ liệu
    const timestamp = new Date().toISOString();
    const dataWithTimestamp = {
      ...data,
      timestamp,
    };

    // Đường dẫn lưu file .txt
    const filePath = path.join(__dirname, 'mqtt_data.txt');
    console.log(filePath);
    // Định dạng chuỗi để ghi vào file
    const dataToWrite = `Received at: ${timestamp}\nData: ${JSON.stringify(dataWithTimestamp, null, 2)}\n\n`;

    try {
      // Kiểm tra xem file đã tồn tại chưa
      await fs.access(filePath)
        .then(() => {
          // Nếu file tồn tại, chỉ cần ghi thêm dữ liệu
          return fs.appendFile(filePath, dataToWrite, 'utf-8');
        })
        .catch(async (err) => {
          // Nếu file không tồn tại, tạo file mới và ghi dữ liệu
          await fs.writeFile(filePath, dataToWrite, 'utf-8');
          this.logger.log('File does not exist. File created and data saved.');
        });

      this.logger.log('Data has been saved to mqtt_data.txt');
    } catch (error) {
      this.logger.error('Failed to save data to file', error);
    }
  }
}
