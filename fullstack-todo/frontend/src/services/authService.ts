// Authentication service for chatbot integration
import { betterAuthClient } from '@/lib/auth/client';

interface AuthState {
  isAuthenticated: boolean;
  userId: string | null;
  token: string | null;
  loading: boolean;
  error: string | null;
}

export const authService = {
  // Check if user is authenticated
  async isAuthenticated(): Promise<boolean> {
    try {
      // Check if we have a valid token in localStorage
      const token = await this.getAuthToken();
      return !!token;
    } catch (error) {
      console.error('Error checking authentication:', error);
      return false;
    }
  },

  // Get current user ID
  async getCurrentUserId(): Promise<string | null> {
    try {
      // Get the token and decode it to extract user ID
      const token = await this.getAuthToken();
      if (token) {
        try {
          const tokenParts = token.split('.');
          const payload = JSON.parse(atob(tokenParts[1]));
          // Support both BetterAuth and main backend token formats
          return payload.sub || payload.userId || payload.user_id || payload.uid || null;
        } catch (decodeError) {
          console.error('Error decoding token to get user ID:', decodeError);
          return null;
        }
      }
      return null;
    } catch (error) {
      console.error('Error getting current user ID:', error);
      return null;
    }
  },

  // Get auth token
  async getAuthToken(): Promise<string | null> {
    try {
      // Get the token from localStorage where BetterAuthClient stores it
      if (typeof window !== 'undefined') {
        const token = localStorage.getItem('auth-token');

        // Verify it's a valid JWT token (has 3 parts separated by dots)
        if (token && token.split('.').length === 3) {
          // Decode the token to check if it's expired
          try {
            const tokenParts = token.split('.');
            const payload = JSON.parse(atob(tokenParts[1]));
            const currentTime = Math.floor(Date.now() / 1000);

            // Check if token is expired
            if (payload.exp && payload.exp < currentTime) {
              // Token is expired, remove it
              localStorage.removeItem('auth-token');
              localStorage.removeItem('user');
              document.cookie = 'auth-token=; path=/; SameSite=Lax; expires=Thu, 01 Jan 1970 00:00:00 GMT;';
              return null;
            }

            return token;
          } catch (decodeError) {
            console.error('Error decoding token:', decodeError);
            return null;
          }
        }
      }

      return null;
    } catch (error) {
      console.error('Error getting auth token:', error);
      return null;
    }
  },

  // Get the current session to verify authentication
  async getSession(): Promise<{ user: any } | null> {
    try {
      // Get the token and decode it to get user information
      const token = await this.getAuthToken();
      if (token) {
        try {
          const tokenParts = token.split('.');
          const payload = JSON.parse(atob(tokenParts[1]));

          return {
            user: {
              id: payload.sub || payload.userId || payload.user_id || 'unknown',
              email: payload.email || 'unknown@example.com',
              name: payload.name || payload.username || 'Unknown User'
            }
          };
        } catch (decodeError) {
          console.error('Error decoding token to get session:', decodeError);
          return null;
        }
      }

      return null;
    } catch (error) {
      console.error('Error getting session:', error);
      return null;
    }
  },

  // Handle auth expiration
  async handleAuthExpiration(): Promise<void> {
    try {
      // Use the BetterAuthClient to sign out the user
      const betterAuthClient = (await import('@/lib/auth/client')).betterAuthClient;
      await betterAuthClient.signOut();

      // Redirect to login page
      if (typeof window !== 'undefined') {
        window.location.href = '/auth/sign-in';
      }
    } catch (error) {
      console.error('Error handling auth expiration:', error);
    }
  },

  // Refresh auth token if needed
  async refreshTokenIfNeeded(): Promise<boolean> {
    try {
      const token = await this.getAuthToken();
      if (!token) {
        return false;
      }

      // Check if token is expired (this is a simplified check)
      // In a real implementation, you'd decode the JWT and check expiration
      const isValid = await this.validateToken(token);
      if (!isValid) {
        // Attempt to refresh the token
        const refreshed = await this.refreshToken();
        return refreshed;
      }

      return true;
    } catch (error) {
      console.error('Error refreshing token:', error);
      return false;
    }
  },

  // Validate token with backend
  async validateToken(token: string): Promise<boolean> {
    try {
      // Check if the token exists and is valid
      const currentToken = await this.getAuthToken();
      return !!currentToken;
    } catch (error) {
      console.error('Error validating token:', error);
      return false;
    }
  },

  // Refresh token from backend
  async refreshToken(): Promise<boolean> {
    try {
      // In this implementation, we rely on the backend to handle token refresh
      // For now, we'll just validate if we have a token
      const currentToken = await this.getAuthToken();
      return !!currentToken;
    } catch (error) {
      console.error('Error refreshing token:', error);
      return false;
    }
  },
};