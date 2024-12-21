// src/user/user.service.ts
import { Injectable } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { CreateUserDto } from './dto/user.dto';
import { User } from './schemas/user.schema'; // Đảm bảo bạn đã tạo schema đúng

@Injectable()
export class UserServices {
  constructor(@InjectModel('User') private readonly userModel: Model<User>) {}

  // Tạo mới user và lưu vào MongoDB
  async create(createUserDto: CreateUserDto) {
    const createdUser = new this.userModel(createUserDto);
    return await createdUser.save();
  }

  // Lấy tất cả người dùng từ MongoDB
  async findAll() {
    return await this.userModel.find().exec();
  }

  // Lấy người dùng theo ID từ MongoDB
  async findOne(id: string) {
    return await this.userModel.findById(id).exec();
  }

  // Cập nhật người dùng theo ID trong MongoDB
  async update(id: string, updateUserDto: CreateUserDto) {
    const updatedUser = await this.userModel.findByIdAndUpdate(id, updateUserDto, {
      new: true, // Trả về đối tượng đã cập nhật
    }).exec();
    return updatedUser;
  }

  // Xóa người dùng theo ID trong MongoDB
  async remove(id: string) {
    const deletedUser = await this.userModel.findByIdAndDelete(id).exec(); // Thay findByIdAndRemove() bằng findByIdAndDelete()
    return deletedUser;
  }
}
