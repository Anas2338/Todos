// API Client Configuration
// This file contains the base configuration for all API calls

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  // Generic request method
  async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;

    // Before making the request, validate that we have a valid token
    const token = this.getAuthToken();
    if (token) {
      // Check if token is valid by decoding it to check expiration
      try {
        const tokenParts = token.split('.');
        if (tokenParts.length === 3) {
          const payload = JSON.parse(atob(tokenParts[1]));
          const currentTime = Math.floor(Date.now() / 1000);

          // If token is expired, remove it from storage
          if (payload.exp && payload.exp < currentTime) {
            console.error('API Client - Token has expired, removing from storage');
            localStorage.removeItem('auth-token');
            localStorage.removeItem('user');
            throw new Error('Token has expired. Please log in again.');
          }
        }
      } catch (decodeError) {
        console.error('API Client - Failed to decode token, removing from storage:', decodeError);
        // If we can't decode the token, remove it
        localStorage.removeItem('auth-token');
        localStorage.removeItem('user');
        throw new Error('Invalid token. Please log in again.');
      }
    } else {
      console.error('API Client - No token found in storage');
    }

    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    // Add auth token if available and Authorization header is not already present
    if (token) {
      const headers = config.headers as Record<string, string>;

      // Check if Authorization header already exists
      if (!headers.Authorization) {
        headers.Authorization = `Bearer ${token}`;
      }
    }

    try {
      // Add timeout to prevent hanging requests
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout

      // Add signal to config object
      const requestConfig = {
        ...config,
        signal: controller.signal
      };

      const response = await fetch(url, requestConfig);
      clearTimeout(timeoutId);

      // If we get a 401 or 403 error, it might mean the token is expired
      // Clear the token and user data to force re-authentication
      if (response.status === 401 || response.status === 403) {
        const errorData = await response.json().catch(() => ({}));
        if (errorData.message) {
          // Clear auth token and user data since the token is likely expired or invalid
          localStorage.removeItem('auth-token');
          localStorage.removeItem('user');
          throw new Error(errorData.message);
        }
      }

      // Handle different response statuses
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error('Response not OK, status:', response.status, 'error data:', errorData);
        throw new Error(errorData.message || `API Error: ${response.status}`);
      }

      // Handle empty responses
      if (response.status === 204) {
        return undefined as T;
      }

      const responseData = await response.json();
      return responseData;
    } catch (error) {
      if (error instanceof Error && error.name === 'AbortError') {
        console.error(`API request timed out: ${url}`);
        throw new Error('Request timed out. Please check your connection and try again.');
      }
      console.error(`API request failed: ${url}`, error);
      throw error;
    }
  }

  // Get auth token from storage or context
  private getAuthToken(): string | null {
    if (typeof window !== 'undefined') {
      // In browser environment
      return localStorage.getItem('auth-token');
    }
    return null;
  }

  // GET request
  get<T>(endpoint: string, options?: RequestInit): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'GET' });
  }

  // POST request
  post<T>(endpoint: string, data?: any, options?: RequestInit): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  // PUT request
  put<T>(endpoint: string, data?: any, options?: RequestInit): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  // PATCH request
  patch<T>(endpoint: string, data?: any, options?: RequestInit): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'PATCH',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  // DELETE request
  async delete<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;

    // Before making the request, validate that we have a valid token
    const token = this.getAuthToken();
    if (token) {
      // Check if token is valid by decoding it to check expiration
      try {
        const tokenParts = token.split('.');
        if (tokenParts.length === 3) {
          const payload = JSON.parse(atob(tokenParts[1]));
          const currentTime = Math.floor(Date.now() / 1000);

          // If token is expired, remove it from storage
          if (payload.exp && payload.exp < currentTime) {
            console.error('API Client DELETE - Token has expired, removing from storage');
            localStorage.removeItem('auth-token');
            localStorage.removeItem('user');
            throw new Error('Token has expired. Please log in again.');
          }
        }
      } catch (decodeError) {
        console.error('API Client DELETE - Failed to decode token, removing from storage:', decodeError);
        // If we can't decode the token, remove it
        localStorage.removeItem('auth-token');
        localStorage.removeItem('user');
        throw new Error('Invalid token. Please log in again.');
      }
    } else {
      console.error('API Client DELETE - No token found in storage');
    }

    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
      ...options,
      method: 'DELETE',
    };

    // Add auth token if available and Authorization header is not already present
    if (token) {
      const headers = config.headers as Record<string, string>;

      // Check if Authorization header already exists
      if (!headers.Authorization) {
        headers.Authorization = `Bearer ${token}`;
      }
    }

    try {
      // Add timeout to prevent hanging requests
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout

      // Add signal to config object
      const requestConfig = {
        ...config,
        signal: controller.signal
      };

      const response = await fetch(url, requestConfig);
      clearTimeout(timeoutId);

      // If we get a 401 or 403 error, it might mean the token is expired
      // Clear the token and user data to force re-authentication
      if (response.status === 401 || response.status === 403) {
        const errorData = await response.json().catch(() => ({}));
        if (errorData.message) {
          // Clear auth token and user data since the token is likely expired or invalid
          localStorage.removeItem('auth-token');
          localStorage.removeItem('user');
          throw new Error(errorData.message);
        }
      }

      // Handle different response statuses
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error('API Client DELETE - Response not OK, status:', response.status, 'error data:', errorData);
        throw new Error(errorData.message || `API Error: ${response.status}`);
      }

      // Handle empty responses (like 204 No Content)
      if (response.status === 204) {
        return undefined as T;
      }

      // For other successful responses, try to parse JSON
      const contentLength = response.headers.get('content-length');
      if (!contentLength || contentLength === '0') {
        // If there's no content, return undefined
        return undefined as T;
      }

      const responseData = await response.json();
      return responseData;
    } catch (error) {
      if (error instanceof Error && error.name === 'AbortError') {
        console.error(`API Client DELETE - Request timed out: ${url}`);
        throw new Error('Request timed out. Please check your connection and try again.');
      }
      console.error(`API Client DELETE - Request failed: ${url}`, error);
      throw error;
    }
  }
}

export const apiClient = new ApiClient();

export default apiClient;