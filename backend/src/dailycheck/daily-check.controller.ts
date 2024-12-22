import { Body, Controller, Delete, Get, Param, Post, Put } from '@nestjs/common';
import { DailyCheckService } from './daily-check.service';
import { CreateDailyCheckDto } from './dto/create-daily-check.dto';
import { DailyCheck } from './schemas/daily-check.schema';

@Controller('daily-check')
export class DailyCheckController {
  constructor(private readonly dailyCheckService: DailyCheckService) {}

  // Route để tạo mới một DailyCheck
  @Post()
  create(@Body() createDailyCheckDto: CreateDailyCheckDto): Promise<DailyCheck> {
    return this.dailyCheckService.create(createDailyCheckDto);
  }

  // Route để lấy tất cả DailyChecks
  @Get()
  findAll(): Promise<DailyCheck[]> {
    return this.dailyCheckService.findAll();
  }

  // Route để cập nhật DailyCheck theo ID
  @Put(':id')
  update(
    @Param('id') id: string,
    @Body() updateDailyCheckDto: CreateDailyCheckDto,
  ): Promise<DailyCheck> {
    return this.dailyCheckService.update(id, updateDailyCheckDto);
  }

  // Route để xóa DailyCheck theo ID
  @Delete(':id')
  remove(@Param('id') id: string): Promise<any> {
    return this.dailyCheckService.remove(id);
  }
}
