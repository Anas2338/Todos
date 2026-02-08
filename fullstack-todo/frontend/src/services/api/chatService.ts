// Chat service for handling communication with the backend

import { Message, Conversation } from '@/types/chat';
import { Todo } from '@/types/todo';
import { betterAuthClient } from '@/lib/auth/client';

// Type guard function to safely check error properties
function isErrorWithProperty<T extends string>(error: unknown, property: T): error is { [K in T]: unknown } {
  return typeof error === 'object' && error !== null && property in error;
}

interface ChatRequest {
  messages: Array<{
    role: 'user';
    content: string;
  }>;
  userId: string;
  conversationId?: string | null;
}

interface ChatResponse {
  choices: Array<{
    index: number;
    message: {
      role: 'assistant';
      content: string;
    };
    finish_reason: string;
  }>;
  todosAffected: Todo[];
  toolCalls: Array<{
    id: string;
    type: 'function';
    function: {
      name: string;
      arguments: string;
    };
  }>;
  conversationId: string;
}

interface ToolCallResponse {
  toolCallId: string;
  result: any;
  status: 'success' | 'error';
  todosAffected: Todo[];
}

class ChatService {
  private static instance: ChatService;
  private baseUrl: string;

  private constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_CHAT_API_URL || '/api/chat';
  }

  public static getInstance(): ChatService {
    if (!ChatService.instance) {
      ChatService.instance = new ChatService();
    }
    return ChatService.instance;
  }

  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    try {
      // Get the auth token from localStorage
      const authToken = localStorage.getItem('auth-token');
      const headers = {
        'Content-Type': 'application/json',
        ...(authToken ? { 'Authorization': `Bearer ${authToken}` } : {}),
      };

      // Add timeout to fetch request
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout

      const response = await fetch(this.baseUrl, {
        method: 'POST',
        headers: authToken
          ? {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${authToken}`
            }
          : {
              'Content-Type': 'application/json'
            },
        body: JSON.stringify({
          messages: request.messages,
          userId: request.userId,
          conversationId: request.conversationId,
        }),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        if (response.status >= 500) {
          throw new Error(`Server error: ${response.status} - ${response.statusText}`);
        } else if (response.status >= 400) {
          throw new Error(`Client error: ${response.status} - ${response.statusText}`);
        } else {
          throw new Error(`Chat API error: ${response.status} - ${response.statusText}`);
        }
      }

      const data: ChatResponse = await response.json();
      return data;
    } catch (error) {
      if (error instanceof TypeError && error.message.includes('fetch')) {
        // Network error (e.g., server unreachable)
        console.error('Network error occurred while sending message:', error);
        throw new Error('Network error: Unable to connect to the server. Please check your internet connection.');
      } else if (isErrorWithProperty(error, 'name') && error.name === 'AbortError') {
        // Request timeout
        console.error('Request timeout while sending message');
        throw new Error('Request timeout: The server took too long to respond.');
      } else if (error instanceof Error) {
        // Other error types (e.g., API errors)
        console.error('Error sending message:', error);
        throw error;
      } else {
        // Unknown error
        console.error('Unknown error occurred while sending message:', error);
        throw new Error('An unknown error occurred while sending the message.');
      }
    }
  }

  async getConversation(conversationId: string): Promise<Conversation> {
    try {
      // Get the auth token from localStorage
      const authToken = localStorage.getItem('auth-token');
      const headers = authToken
        ? { 'Authorization': `Bearer ${authToken}` }
        : { };

      // Add timeout to fetch request
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout

      const response = await fetch(`${this.baseUrl}/conversation/${conversationId}`, {
        method: 'GET',
        headers: authToken
          ? { 'Authorization': `Bearer ${authToken}` }
          : { },
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        if (response.status >= 500) {
          throw new Error(`Server error: ${response.status} - ${response.statusText}`);
        } else if (response.status >= 400) {
          throw new Error(`Client error: ${response.status} - ${response.statusText}`);
        } else {
          throw new Error(`Failed to get conversation: ${response.status} - ${response.statusText}`);
        }
      }

      const data: Conversation = await response.json();
      return data;
    } catch (error) {
      if (error instanceof TypeError && error.message.includes('fetch')) {
        // Network error (e.g., server unreachable)
        console.error('Network error occurred while getting conversation:', error);
        throw new Error('Network error: Unable to connect to the server. Please check your internet connection.');
      } else if (isErrorWithProperty(error, 'name') && error.name === 'AbortError') {
        // Request timeout
        console.error('Request timeout while getting conversation');
        throw new Error('Request timeout: The server took too long to respond.');
      } else if (error instanceof Error) {
        // Other error types (e.g., API errors)
        console.error('Error getting conversation:', error);
        throw error;
      } else {
        // Unknown error
        console.error('Unknown error occurred while getting conversation:', error);
        throw new Error('An unknown error occurred while getting the conversation.');
      }
    }
  }

  async getMessages(conversationId: string): Promise<Message[]> {
    try {
      // Get the auth token from localStorage
      const authToken = localStorage.getItem('auth-token');
      const headers = authToken ? { 'Authorization': `Bearer ${authToken}` } : {};

      // Add timeout to fetch request
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout

      const response = await fetch(`${this.baseUrl}/messages/${conversationId}`, {
        method: 'GET',
        headers: authToken
          ? { 'Authorization': `Bearer ${authToken}` }
          : { },
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        if (response.status >= 500) {
          throw new Error(`Server error: ${response.status} - ${response.statusText}`);
        } else if (response.status >= 400) {
          throw new Error(`Client error: ${response.status} - ${response.statusText}`);
        } else {
          throw new Error(`Failed to get messages: ${response.status} - ${response.statusText}`);
        }
      }

      const data: Message[] = await response.json();
      return data;
    } catch (error) {
      if (error instanceof TypeError && error.message.includes('fetch')) {
        // Network error (e.g., server unreachable)
        console.error('Network error occurred while getting messages:', error);
        throw new Error('Network error: Unable to connect to the server. Please check your internet connection.');
      } else if (isErrorWithProperty(error, 'name') && error.name === 'AbortError') {
        // Request timeout
        console.error('Request timeout while getting messages');
        throw new Error('Request timeout: The server took too long to respond.');
      } else if (error instanceof Error) {
        // Other error types (e.g., API errors)
        console.error('Error getting messages:', error);
        throw error;
      } else {
        // Unknown error
        console.error('Unknown error occurred while getting messages:', error);
        throw new Error('An unknown error occurred while getting the messages.');
      }
    }
  }

  async handleToolCall(toolCallId: string, result: any): Promise<ToolCallResponse> {
    try {
      // Get the auth token from localStorage
      const authToken = localStorage.getItem('auth-token');
      const headers = {
        'Content-Type': 'application/json',
        ...(authToken ? { 'Authorization': `Bearer ${authToken}` } : {}),
      };

      // Add timeout to fetch request
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout

      const response = await fetch(`${this.baseUrl}/tool-calls/${toolCallId}`, {
        method: 'POST',
        headers: authToken
          ? {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${authToken}`
            }
          : {
              'Content-Type': 'application/json'
            },
        body: JSON.stringify({ result }),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        if (response.status >= 500) {
          throw new Error(`Server error: ${response.status} - ${response.statusText}`);
        } else if (response.status >= 400) {
          throw new Error(`Client error: ${response.status} - ${response.statusText}`);
        } else {
          throw new Error(`Failed to handle tool call: ${response.status} - ${response.statusText}`);
        }
      }

      const data: ToolCallResponse = await response.json();
      return data;
    } catch (error) {
      if (error instanceof TypeError && error.message.includes('fetch')) {
        // Network error (e.g., server unreachable)
        console.error('Network error occurred while handling tool call:', error);
        throw new Error('Network error: Unable to connect to the server. Please check your internet connection.');
      } else if (isErrorWithProperty(error, 'name') && error.name === 'AbortError') {
        // Request timeout
        console.error('Request timeout while handling tool call');
        throw new Error('Request timeout: The server took too long to respond.');
      } else if (error instanceof Error) {
        // Other error types (e.g., API errors)
        console.error('Error handling tool call:', error);
        throw error;
      } else {
        // Unknown error
        console.error('Unknown error occurred while handling tool call:', error);
        throw new Error('An unknown error occurred while handling the tool call.');
      }
    }
  }

  async createConversation(userId: string): Promise<Conversation> {
    try {
      // Get the auth token from localStorage
      const authToken = localStorage.getItem('auth-token');
      const headers = {
        'Content-Type': 'application/json',
        ...(authToken ? { 'Authorization': `Bearer ${authToken}` } : {}),
      };

      // Add timeout to fetch request
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout

      const response = await fetch(`${this.baseUrl}/conversations`, {
        method: 'POST',
        headers: authToken
          ? {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${authToken}`
            }
          : {
              'Content-Type': 'application/json'
            },
        body: JSON.stringify({ userId }),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        if (response.status >= 500) {
          throw new Error(`Server error: ${response.status} - ${response.statusText}`);
        } else if (response.status >= 400) {
          throw new Error(`Client error: ${response.status} - ${response.statusText}`);
        } else {
          throw new Error(`Failed to create conversation: ${response.status} - ${response.statusText}`);
        }
      }

      const data: Conversation = await response.json();
      return data;
    } catch (error) {
      if (error instanceof TypeError && error.message.includes('fetch')) {
        // Network error (e.g., server unreachable)
        console.error('Network error occurred while creating conversation:', error);
        throw new Error('Network error: Unable to connect to the server. Please check your internet connection.');
      } else if (isErrorWithProperty(error, 'name') && error.name === 'AbortError') {
        // Request timeout
        console.error('Request timeout while creating conversation');
        throw new Error('Request timeout: The server took too long to respond.');
      } else if (error instanceof Error) {
        // Other error types (e.g., API errors)
        console.error('Error creating conversation:', error);
        throw error;
      } else {
        // Unknown error
        console.error('Unknown error occurred while creating conversation:', error);
        throw new Error('An unknown error occurred while creating the conversation.');
      }
    }
  }
}

export const chatService = ChatService.getInstance();