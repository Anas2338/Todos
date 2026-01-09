import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { User } from '@/types/auth';
import { betterAuthClient } from '@/lib/auth/client';

interface UseAuthReturn {
  user: User | null;
  loading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  register: (email: string, password: string, name?: string) => Promise<void>;
}

export const useAuth = (): UseAuthReturn => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    // Check for existing session on mount
    const checkSession = async () => {
      try {
        // Wait a bit to ensure the DOM is ready
        await new Promise(resolve => setTimeout(resolve, 50));

        const session = await betterAuthClient.getSession();
        if (session && session.user) {
          setUser({
            id: session.user.id,
            email: session.user.email,
            name: session.user.name,
            createdAt: session.user.createdAt || new Date(),
            updatedAt: session.user.updatedAt || new Date()
          });
        }
      } catch (err) {
        console.error('Session check failed:', err);
        setError('Failed to check session');
      } finally {
        // Ensure loading is set to false after initial check
        setLoading(false);
      }
    };

    checkSession();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      setLoading(true);
      setError(null);

      // Clear any existing auth data before login to prevent conflicts
      localStorage.removeItem('auth-token');
      localStorage.removeItem('user');

      const response = await betterAuthClient.signIn({ email, password });

      // Wait a bit to ensure the auth data is stored
      await new Promise(resolve => setTimeout(resolve, 200));

      // Verify the session is properly established with retries
      let session = null;
      let attempts = 0;
      const maxAttempts = 5;

      while (attempts < maxAttempts) {
        session = await betterAuthClient.getSession();

        if (session && session.user) {
          // Successfully got the session, set the user state
          setUser({
            id: session.user.id,
            email: session.user.email || email,
            name: session.user.name || undefined,
            createdAt: session.user.createdAt || new Date(),
            updatedAt: session.user.updatedAt || new Date()
          });

          // Wait a little more to ensure state is updated before redirect
          await new Promise(resolve => setTimeout(resolve, 100));
          break;
        }

        attempts++;
        if (attempts < maxAttempts) {
          // Wait before next attempt
          await new Promise(resolve => setTimeout(resolve, 200));
        }
      }

      if (!session || !session.user) {
        // If we still can't get the session, use the response data as fallback
        setUser({
          id: response.user_id,
          email,
          createdAt: new Date(),
          updatedAt: new Date()
        });
      }

      // Redirect to dashboard after successful login and session establishment
      router.push('/dashboard');
    } catch (err) {
      setError((err as Error).message || 'Login failed');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const register = async (email: string, password: string, name?: string) => {
    try {
      setLoading(true);
      setError(null);

      // Clear any existing auth data before registration to prevent conflicts
      localStorage.removeItem('auth-token');
      localStorage.removeItem('user');

      // First, register the user
      const userData = await betterAuthClient.signUp({ email, password, name });

      // Then, sign in the user with the same credentials to establish a session
      const response = await betterAuthClient.signIn({ email, password });

      // Wait a bit to ensure the auth data is stored
      await new Promise(resolve => setTimeout(resolve, 200));

      // Verify the session is properly established with retries
      let session = null;
      let attempts = 0;
      const maxAttempts = 5;

      while (attempts < maxAttempts) {
        session = await betterAuthClient.getSession();

        if (session && session.user) {
          // Successfully got the session, set the user state
          setUser({
            id: session.user.id,
            email: session.user.email || email,
            name: session.user.name || name,
            createdAt: session.user.createdAt || new Date(),
            updatedAt: session.user.updatedAt || new Date()
          });

          // Wait a little more to ensure state is updated before redirect
          await new Promise(resolve => setTimeout(resolve, 100));
          break;
        }

        attempts++;
        if (attempts < maxAttempts) {
          // Wait before next attempt
          await new Promise(resolve => setTimeout(resolve, 200));
        }
      }

      if (!session || !session.user) {
        // If we still can't get the session, use the response data as fallback
        setUser({
          id: response.user_id,
          email,
          name: name,
          createdAt: new Date(),
          updatedAt: new Date()
        });
      }

      // Redirect to dashboard after successful registration and login
      router.push('/dashboard');
    } catch (err) {
      setError((err as Error).message || 'Registration failed');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    try {
      setLoading(true);
      setError(null);

      await betterAuthClient.signOut();

      // Clear user state immediately
      setUser(null);

      // Additional cleanup to ensure everything is cleared
      localStorage.removeItem('auth-token');
      localStorage.removeItem('user');
      document.cookie = 'auth-token=; path=/; SameSite=Lax; expires=Thu, 01 Jan 1970 00:00:00 GMT;';

      // Wait a moment to ensure all cleanup is complete
      await new Promise(resolve => setTimeout(resolve, 100));

      router.push('/login');
    } catch (err) {
      setError((err as Error).message || 'Logout failed');
      console.error('Logout error:', err);
    } finally {
      setLoading(false);
    }
  };

  return {
    user,
    loading,
    error,
    login,
    logout,
    register,
  };
};