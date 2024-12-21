import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { HttpModule } from './http/http.module';
import { MongooseModule } from '@nestjs/mongoose';
import { DatabaseModule } from './database/database.module';
import { UserModule } from './user/user.module';
import { MedicalModule } from './medical/medical.module';
@Module({
  imports: [
    MongooseModule.forRoot('mongodb+srv://tanghvinfo:bhXe73BqgvB2QgTk@clusterlife.kc56d.mongodb.net/hust_life'),
    HttpModule,
    DatabaseModule,
    UserModule,
    MedicalModule
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
