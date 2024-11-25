import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document } from 'mongoose';

// Định nghĩa Schema cho User
@Schema()
export class User extends Document {
  @Prop({ required: true })
  name: string;

  @Prop({ required: true, unique: true })
  email: string;

  @Prop({ required: true })
  password: string;

  @Prop({ required: true })
  age: number;

  @Prop({ required: true })
  height: number; // Chiều cao tính theo cm (ví dụ: 175)

  @Prop({ required: true })
  weight: number; // Cân nặng tính theo kg (ví dụ: 70)

  @Prop({ required: true })
  avatar: string; // Link đến hình ảnh avatar
}

export const UserSchema = SchemaFactory.createForClass(User);
