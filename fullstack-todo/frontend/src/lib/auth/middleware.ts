// Session management utilities for the frontend application

// Check if the session is expired based on the token's expiration time
export function isSessionExpired(token: string | null): boolean {
  if (!token) {
    return true;
  }

  try {
    // Decode JWT token to check expiration
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );

    const { exp } = JSON.parse(jsonPayload);
    const currentTime = Math.floor(Date.now() / 1000);

    return exp < currentTime;
  } catch (error) {
    console.error('Error checking session expiration:', error);
    return true;
  }
}

// Get the expiration time of the session
export function getSessionExpiration(token: string | null): Date | null {
  if (!token) {
    return null;
  }

  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );

    const { exp } = JSON.parse(jsonPayload);
    return new Date(exp * 1000);
  } catch (error) {
    console.error('Error getting session expiration:', error);
    return null;
  }
}

// Refresh the session token
export async function refreshSession(): Promise<string | null> {
  try {
    const response = await fetch('/api/auth/refresh', {
      method: 'POST',
      credentials: 'include',
    });

    if (response.ok) {
      const { access_token } = await response.json();
      // Store the new token
      if (typeof window !== 'undefined') {
        localStorage.setItem('auth-token', access_token);
      }
      return access_token;
    }

    throw new Error('Session refresh failed');
  } catch (error) {
    console.error('Error refreshing session:', error);
    return null;
  }
}

// Set up automatic session refresh before expiration
export function setupSessionRefresh(
  onSessionExpired?: () => void,
  refreshBeforeSeconds: number = 60
): () => void {
  let timeoutId: NodeJS.Timeout | null = null;

  const checkAndRefreshSession = async () => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('auth-token') : null;

    if (token) {
      const expiration = getSessionExpiration(token);

      if (expiration) {
        const timeUntilExpiration = expiration.getTime() - Date.now();
        const refreshTime = timeUntilExpiration - refreshBeforeSeconds * 1000;

        if (refreshTime <= 0) {
          // Session is expired or about to expire
          const newToken = await refreshSession();

          if (!newToken) {
            // Refresh failed, session has expired
            if (onSessionExpired) {
              onSessionExpired();
            }
            return;
          }
        }

        // Schedule next check
        timeoutId = setTimeout(checkAndRefreshSession, Math.max(0, refreshTime));
      }
    }
  };

  // Initial check
  checkAndRefreshSession();

  // Return cleanup function
  return () => {
    if (timeoutId) {
      clearTimeout(timeoutId);
    }
  };
}

// Clear all session data
export function clearSession(): void {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('auth-token');
    localStorage.removeItem('user-data');
    localStorage.removeItem('refresh-token');
  }
}