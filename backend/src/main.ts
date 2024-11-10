import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Bật CORS để cho phép frontend từ các nguồn khác gọi API
  app.enableCors({
    origin: 'http://localhost:3000', // Chỉ cho phép frontend trên localhost:3000 gọi
    methods: 'GET, POST, PUT, DELETE', // Các phương thức HTTP được phép
    allowedHeaders: 'Content-Type, Accept', // Các header được phép
  });

  await app.listen(4000); // Cổng của backend
}
bootstrap();
