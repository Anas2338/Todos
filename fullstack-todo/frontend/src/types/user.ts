// Type definitions for user-related entities

export interface User {
  id: string;
  email: string;
  name: string;
  createdAt: Date;
  lastLoginAt: Date;
}

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  token: string | null;
  refreshToken: string | null;
}

export interface AuthCredentials {
  email: string;
  password: string;
}

export interface AuthResponse {
  user: User;
  token: string;
  refreshToken: string;
}

export interface Session {
  userId: string;
  sessionId: string;
  expiresAt: Date;
  token: string;
}