// API service for chatbot functionality
import { ChatRequest, ChatResponse, Message } from '@/types/chat';
import { authService } from './authService';

const CHAT_API_BASE = process.env.NEXT_PUBLIC_CHAT_API_URL || 'http://localhost:8001/api/v1/chat';

interface SendMessageRequest {
  message: string;
  conversationId?: string;
}

interface SendMessageResponse {
  success: boolean;
  session_id: string;
  response: string;
  timestamp?: string;
}

interface GetHistoryRequest {
  conversationId: string;
}

interface GetHistoryResponse {
  messages: {
    id: string;
    role: string;
    content: string;
    timestamp: string;
  }[];
  total_count: number;
}

interface StartConversationResponse {
  success: boolean;
  session_id: string;
  response?: string;
  timestamp?: string;
}

interface GetConversationsResponse {
  sessions: {
    id: string;
    title: string;
    created_at: string;
    updated_at: string;
    is_active: boolean;
  }[];
  total_count: number;
}

interface ErrorResponse {
  success: false;
  error: string;
  errorCode?: string;
  retryable?: boolean;
}

export const chatApi = {
  async sendMessage(data: SendMessageRequest): Promise<SendMessageResponse | ErrorResponse> {
    try {
      // Check if user is properly authenticated
      const isAuthenticated = await authService.isAuthenticated();

      let authHeaders = {};
      if (isAuthenticated) {
        authHeaders = await getAuthHeaders();
      }

      const response = await fetch(`${CHAT_API_BASE}/sessions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // Include authentication headers if available
          ...authHeaders,
        },
        body: JSON.stringify({
          message: data.message,
          session_id: data.conversationId || null,
        }),
      });

      if (!response.ok) {
        // Don't treat 401 as an error to be logged since it's expected when not authenticated
        if (response.status === 401) {
          // Return an error response indicating authentication is required
          return {
            success: false,
            error: 'Authentication required. Please log in to send messages.',
            errorCode: 'UNAUTHORIZED',
            retryable: false,
          };
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result: SendMessageResponse | ErrorResponse = await response.json();
      return result;
    } catch (error) {
      // Only log errors that aren't 401 Unauthorized
      if (!(error instanceof Error && error.message.includes('401'))) {
        console.error('Error sending message:', error);
      }
      return {
        success: false,
        error: 'Failed to send message. Please try again.',
        retryable: true,
      };
    }
  },

  async getHistory(request: GetHistoryRequest): Promise<GetHistoryResponse | ErrorResponse> {
    try {
      // Check if user is properly authenticated
      const isAuthenticated = await authService.isAuthenticated();

      let authHeaders = {};
      if (isAuthenticated) {
        authHeaders = await getAuthHeaders();
      }

      const response = await fetch(
        `${CHAT_API_BASE}/sessions/${encodeURIComponent(request.conversationId)}/messages`,
        {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            ...authHeaders,
          },
        }
      );

      if (!response.ok) {
        // Don't treat 401 as an error to be logged since it's expected when not authenticated
        if (response.status === 401) {
          return {
            success: false,
            error: 'Authentication required. Please log in to access conversations.',
            errorCode: 'UNAUTHORIZED',
            retryable: false,
          };
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result: GetHistoryResponse | ErrorResponse = await response.json();
      return result;
    } catch (error) {
      // Only log errors that aren't 401 Unauthorized
      if (!(error instanceof Error && error.message.includes('401'))) {
        console.error('Error getting history:', error);
      }
      return {
        success: false,
        error: 'Failed to retrieve conversation history. Please try again.',
        retryable: true,
      };
    }
  },

  async startConversation(): Promise<StartConversationResponse | ErrorResponse> {
    try {
      // Check if user is properly authenticated
      const isAuthenticated = await authService.isAuthenticated();

      let authHeaders = {};
      if (isAuthenticated) {
        authHeaders = await getAuthHeaders();
      }

      const response = await fetch(`${CHAT_API_BASE}/sessions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...authHeaders,
        },
        body: JSON.stringify({
          message: "New conversation started",
          session_id: null
        }),
      });

      if (!response.ok) {
        // Don't treat 401 as an error to be logged since it's expected when not authenticated
        if (response.status === 401) {
          return {
            success: false,
            error: 'Authentication required. Please log in to start conversations.',
            errorCode: 'UNAUTHORIZED',
            retryable: false,
          };
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result: StartConversationResponse | ErrorResponse = await response.json();
      return result;
    } catch (error) {
      // Only log errors that aren't 401 Unauthorized
      if (!(error instanceof Error && error.message.includes('401'))) {
        console.error('Error starting conversation:', error);
      }
      return {
        success: false,
        error: 'Failed to start conversation. Please try again.',
        retryable: true,
      };
    }
  },

  async getConversations(): Promise<GetConversationsResponse | ErrorResponse> {
    try {
      // Check if user is properly authenticated
      const isAuthenticated = await authService.isAuthenticated();

      let authHeaders = {};
      if (isAuthenticated) {
        authHeaders = await getAuthHeaders();
      }

      const response = await fetch(`${CHAT_API_BASE}/sessions`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          ...authHeaders,
        },
      });

      if (!response.ok) {
        // Don't treat 401 as an error to be logged since it's expected when not authenticated
        if (response.status === 401) {
          return {
            success: false,
            error: 'Authentication required. Please log in to access conversations.',
            errorCode: 'UNAUTHORIZED',
            retryable: false,
          };
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result: GetConversationsResponse | ErrorResponse = await response.json();
      return result;
    } catch (error) {
      // Only log errors that aren't 401 Unauthorized
      if (!(error instanceof Error && error.message.includes('401'))) {
        console.error('Error getting conversations:', error);
      }
      return {
        success: false,
        error: 'Failed to retrieve conversations. Please try again.',
        retryable: true,
      };
    }
  },
};

// Helper function to get auth headers
async function getAuthHeaders(): Promise<Record<string, string>> {
  // Get the auth token from the auth service
  const token = await authService.getAuthToken();

  if (token) {
    return { Authorization: `Bearer ${token}` };
  }

  return {};
}