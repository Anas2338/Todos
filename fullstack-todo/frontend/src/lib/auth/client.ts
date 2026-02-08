// Better Auth client configuration for the frontend application
// This implementation connects to the real authentication service on port 8000

export class BetterAuthClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_BETTER_AUTH_URL || 'http://localhost:8000';
  }

  // Initialize the auth client
  async init() {
    // Implementation would depend on the specific Better Auth library
    console.log('Better Auth client initialized');
  }

  // Get current session - retrieve stored user info from localStorage and validate token
  async getSession() {
    // Implementation would handle session retrieval
    try {
      // Get token and user info from localStorage
      const token = localStorage.getItem('auth-token');
      const userStr = localStorage.getItem('user');

      if (!token || !userStr) {
        return null;
      }

      // Validate the token by decoding it to check if it's still valid
      const user = JSON.parse(userStr);

      try {
        const tokenParts = token.split('.');
        if (tokenParts.length !== 3) {
          // Invalid JWT format
          localStorage.removeItem('auth-token');
          localStorage.removeItem('user');
          // Also remove the cookie
          document.cookie = 'auth-token=; path=/; SameSite=Lax; expires=Thu, 01 Jan 1970 00:00:00 GMT;';
          return null;
        }

        // Decode the payload (second part)
        const payload = JSON.parse(atob(tokenParts[1]));
        const currentTime = Math.floor(Date.now() / 1000);

        // Check if token is expired
        if (payload.exp && payload.exp < currentTime) {
          // Token is expired, remove from storage
          localStorage.removeItem('auth-token');
          localStorage.removeItem('user');
          // Also remove the cookie
          document.cookie = 'auth-token=; path=/; SameSite=Lax; expires=Thu, 01 Jan 1970 00:00:00 GMT;';
          return null;
        }

        // Check if the user ID in the token matches the user ID in localStorage
        // This ensures consistency between token and stored user data
        if (payload.sub && user.id) {
          // Only compare if both values exist and are non-empty
          const tokenUserId = String(payload.sub).trim();
          const storedUserId = String(user.id).trim();

          if (tokenUserId && storedUserId && tokenUserId !== storedUserId) {
            console.warn('User ID mismatch between token and stored data. Clearing auth data.');
            console.warn(`Token user ID: ${tokenUserId}, Stored user ID: ${storedUserId}`);
            localStorage.removeItem('auth-token');
            localStorage.removeItem('user');
            // Also remove the cookie
            document.cookie = 'auth-token=; path=/; SameSite=Lax; expires=Thu, 01 Jan 1970 00:00:00 GMT;';
            return null;
          }
        }

        // Update the cookie to ensure it's still valid (refresh the cookie)
        document.cookie = `auth-token=${token}; path=/; max-age=86400; SameSite=Lax`; // 24 hours

        return { user };
      } catch (decodeError) {
        console.error('Error decoding token:', decodeError);
        // If we can't decode the token, remove it from storage
        localStorage.removeItem('auth-token');
        localStorage.removeItem('user');
        // Also remove the cookie
        document.cookie = 'auth-token=; path=/; SameSite=Lax; expires=Thu, 01 Jan 1970 00:00:00 GMT;';
        return null;
      }
    } catch (error) {
      console.error('Error getting session:', error);
      return null;
    }
  }

  // Sign in user
  async signIn(credentials: { email: string; password: string }) {
    try {
      // Clear any existing auth data before login to prevent conflicts
      localStorage.removeItem('auth-token');
      localStorage.removeItem('user');

      const response = await fetch(`${this.baseUrl}/auth/signin`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      });

      if (response.ok) {
        const result = await response.json();
        // Store the token in localStorage
        if (result.access_token) {
          localStorage.setItem('auth-token', result.access_token);
          // Also set the token as a cookie so the middleware can access it
          document.cookie = `auth-token=${result.access_token}; path=/; max-age=1800; SameSite=Lax`; // 30 minutes (matches backend config)

          // Store user info if available
          if (result.user_id) {
            localStorage.setItem('user', JSON.stringify({
              id: result.user_id,
              email: credentials.email
            }));
          }
        }
        return result;
      } else {
        // Get error details from response
        let errorMessage = 'Login failed';
        try {
          const errorData = await response.json();
          if (errorData.message) {
            errorMessage = errorData.message;
          } else if (errorData.detail) {
            errorMessage = Array.isArray(errorData.detail)
              ? errorData.detail.map((e: any) => e.msg).join(', ')
              : errorData.detail;
          }
        } catch (e) {
          // If we can't parse the error response, use the status text
          errorMessage = `Login failed: ${response.statusText}`;
        }
        throw new Error(errorMessage);
      }
    } catch (error) {
      console.error('Sign in error:', error);
      throw error;
    }
  }

  // Sign up user
  async signUp(credentials: { email: string; password: string; name?: string }) {
    try {
      // Only send email and password to match backend expectations
      const requestPayload = {
        email: credentials.email,
        password: credentials.password
      };

      const response = await fetch(`${this.baseUrl}/auth/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestPayload),
      });

      if (response.ok) {
        const result = await response.json();
        // Store user info in localStorage after registration
        if (result.id) {
          localStorage.setItem('user', JSON.stringify({
            id: result.id,
            email: result.email
          }));
        }
        // Note: Signup doesn't return an access token, so no cookie is set here
        // The user would need to sign in after registration to get an access token
        return result;
      } else {
        // Get error details from response
        let errorMessage = 'Registration failed';
        try {
          const errorData = await response.json();
          if (errorData.message) {
            errorMessage = errorData.message;
          } else if (errorData.detail) {
            errorMessage = Array.isArray(errorData.detail)
              ? errorData.detail.map((e: any) => e.msg).join(', ')
              : errorData.detail;
          }
        } catch (e) {
          // If we can't parse the error response, use the status text
          errorMessage = `Registration failed: ${response.statusText}`;
        }
        throw new Error(errorMessage);
      }
    } catch (error) {
      console.error('Sign up error:', error);
      throw error;
    }
  }

  // Sign out user
  async signOut() {
    try {
      // Clear user data from localStorage
      localStorage.removeItem('auth-token');
      localStorage.removeItem('user');

      // Also remove the auth-token cookie
      document.cookie = 'auth-token=; path=/; SameSite=Lax; expires=Thu, 01 Jan 1970 00:00:00 GMT;';

      return true;
    } catch (error) {
      console.error('Sign out error:', error);
      throw error;
    }
  }
}

// Export a singleton instance
export const betterAuthClient = new BetterAuthClient();