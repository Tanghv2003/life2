import { Injectable } from '@nestjs/common';
import { Esp32Dto } from './dto/esp32data.dto';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { Esp32Data } from './schemas/esp32data.schema';

@Injectable()
export class HttpServices{

    constructor(
        @InjectModel('Esp32Data') private readonly esp32DataModel: Model<Esp32Data>,
    ) {}

    processData(data : Esp32Dto) : string {
        console.log('Dữ liệu nhận từ ESP32:', data);
        return `${data.temperature}`;
    }

    async saveEsp32Data(esp32Dto: Esp32Dto): Promise<Esp32Data> {
        const createdEsp32Data = new this.esp32DataModel(esp32Dto);
        return createdEsp32Data.save();
      }
}