// src/medical/schemas/medical.schema.ts

import { Schema, Document } from 'mongoose';

export const MedicalRecordSchema = new Schema({
  heartDisease: { type: Boolean, required: false },
  bmi: { type: Number, required: false },
  smoking: { type: Boolean, required: false },
  alcoholDrinking: { type: Boolean, required: false },
  stroke: { type: Boolean, required: false },
  physicalHealth: { type: Number, required: false },
  mentalHealth: { type: Number, required: false },
  diffWalking: { type: Boolean, required: false },
  sex: { type: String, required: false },
  ageCategory: { type: String, required: false },
  race: { type: String, required: false },
  diabetic: { type: Boolean, required: false },
  physicalActivity: { type: Boolean, required: false },
  genHealth: { type: String, required: false },
  sleepTime: { type: Number, required: false },
  asthma: { type: Boolean, required: false },
  kidneyDisease: { type: Boolean, required: false },
  skinCancer: { type: Boolean, required: false },
});

export interface MedicalRecord extends Document {
  heartDisease: boolean;
  bmi: number;
  smoking: boolean;
  alcoholDrinking: boolean;
  stroke: boolean;
  physicalHealth: number;
  mentalHealth: number;
  diffWalking: boolean;
  sex: string;
  ageCategory: string;
  race: string;
  diabetic: boolean;
  physicalActivity: boolean;
  genHealth: string;
  sleepTime: number;
  asthma: boolean;
  kidneyDisease: boolean;
  skinCancer: boolean;
}
