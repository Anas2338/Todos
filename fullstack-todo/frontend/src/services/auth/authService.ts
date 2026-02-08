// Authentication service for Better Auth integration

import { User, AuthCredentials, AuthResponse, Session } from '@/types/user';

class AuthService {
  private static instance: AuthService;
  private currentUser: User | null = null;
  private authToken: string | null = null;

  private constructor() {}

  public static getInstance(): AuthService {
    if (!AuthService.instance) {
      AuthService.instance = new AuthService();
    }
    return AuthService.instance;
  }

  async login(credentials: AuthCredentials): Promise<AuthResponse> {
    try {
      // This would integrate with Better Auth API
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      });

      if (!response.ok) {
        throw new Error('Authentication failed');
      }

      const data: AuthResponse = await response.json();
      this.authToken = data.token;
      this.currentUser = data.user;

      return data;
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  }

  async logout(): Promise<void> {
    try {
      await fetch('/api/auth/logout', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.authToken}`,
        },
      });

      this.currentUser = null;
      this.authToken = null;
    } catch (error) {
      console.error('Logout error:', error);
      // Still clear local state even if API call fails
      this.currentUser = null;
      this.authToken = null;
    }
  }

  async getCurrentUser(): Promise<User | null> {
    if (this.currentUser) {
      return this.currentUser;
    }

    if (this.authToken) {
      try {
        const response = await fetch('/api/auth/me', {
          headers: {
            'Authorization': `Bearer ${this.authToken}`,
          },
        });

        if (response.ok) {
          const user: User = await response.json();
          this.currentUser = user;
          return user;
        }
      } catch (error) {
        console.error('Error getting current user:', error);
      }
    }

    return null;
  }

  async isAuthenticated(): Promise<boolean> {
    const user = await this.getCurrentUser();
    return user !== null;
  }

  getAuthToken(): string | null {
    return this.authToken;
  }

  async refreshToken(): Promise<string | null> {
    if (!this.authToken) {
      return null;
    }

    try {
      const response = await fetch('/api/auth/refresh', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.authToken}`,
        },
      });

      if (response.ok) {
        const data: AuthResponse = await response.json();
        this.authToken = data.token;
        return data.token;
      } else {
        // If refresh fails, clear the token
        this.authToken = null;
        return null;
      }
    } catch (error) {
      console.error('Token refresh error:', error);
      return null;
    }
  }

  // Method to add auth headers to requests
  addAuthHeader(headers: HeadersInit = {}): HeadersInit {
    if (this.authToken) {
      return {
        ...headers,
        'Authorization': `Bearer ${this.authToken}`,
      };
    }
    return headers;
  }
}

export const authService = AuthService.getInstance();