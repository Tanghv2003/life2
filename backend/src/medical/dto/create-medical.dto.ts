// src/medical/dto/create-medical.dto.ts

import { IsBoolean, IsEnum, IsNumber, IsOptional, IsString } from 'class-validator';

export class CreateMedicalDto {
  @IsOptional()
  @IsBoolean()
  heartDisease: boolean;

  @IsOptional()
  @IsNumber()
  bmi: number;

  @IsOptional()
  @IsBoolean()
  smoking: boolean;

  @IsOptional()
  @IsBoolean()
  alcoholDrinking: boolean;

  @IsOptional()
  @IsBoolean()
  stroke: boolean;

  @IsOptional()
  @IsNumber()
  physicalHealth: number;

  @IsOptional()
  @IsNumber()
  mentalHealth: number;

  @IsOptional()
  @IsBoolean()
  diffWalking: boolean;

  @IsOptional()
  @IsString()
  sex: string;

  @IsOptional()
  @IsString()
  ageCategory: string;

  @IsOptional()
  @IsString()
  race: string;

  @IsOptional()
  @IsBoolean()
  diabetic: boolean;

  @IsOptional()
  @IsBoolean()
  physicalActivity: boolean;

  @IsOptional()
  @IsString()
  genHealth: string;

  @IsOptional()
  @IsNumber()
  sleepTime: number;

  @IsOptional()
  @IsBoolean()
  asthma: boolean;

  @IsOptional()
  @IsBoolean()
  kidneyDisease: boolean;

  @IsOptional()
  @IsBoolean()
  skinCancer: boolean;
}
