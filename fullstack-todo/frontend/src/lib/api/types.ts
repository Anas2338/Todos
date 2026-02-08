// API response types for the frontend application

export interface ApiResponse<T = any> {
  data?: T;
  error?: string;
  message?: string;
  status: number;
}

export interface TaskApiResponse {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  userId: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface TaskListApiResponse {
  tasks: TaskApiResponse[];
}

export interface AuthApiResponse {
  id: string;
  email: string;
  name?: string;
}

export interface LoginApiResponse {
  access_token: string;
  token_type: string;
  user_id: string;
}

export interface ErrorApiResponse {
  error_code: string;
  message: string;
  timestamp: string;
}