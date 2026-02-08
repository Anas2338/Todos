import { useState, useCallback, useEffect } from 'react';
import { Message, ChatState } from '@/types/chat';
import { chatApi } from '@/services/chatApi';
import { authService } from '@/services/authService';
import {
  isValidMessage,
  isUserMessage,
  isAssistantMessage,
  sanitizeMessageContent,
  generateMessageId,
  generateConversationId
} from '@/utils/chatUtils';

interface UseChatBotReturn {
  messages: Message[];
  isLoading: boolean;
  currentInput: string;
  error: string | null;
  sendMessage: (message: string) => Promise<void>;
  setCurrentInput: (input: string) => void;
  clearMessages: () => void;
  reconnect: () => void;
  checkAuthAndRedirect: () => Promise<boolean>;
}

export const useChatBot = (): UseChatBotReturn => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [currentInput, setCurrentInput] = useState<string>('');
  const [error, setError] = useState<string | null>(null);

  // Initialize the chat
  useEffect(() => {
    initializeChat();
  }, []);

  const initializeChat = async () => {
    try {
      const isAuthenticated = await authService.isAuthenticated();
      // Don't set error if not authenticated, just continue without full functionality
      if (!isAuthenticated) {
        // Optionally set a status message instead of error
        // setError('User not authenticated. Please log in to access the chatbot.');
      }
    } catch (err) {
      // Don't set error for initialization issues, just log them
      console.error('Error initializing chat:', err);
    }
  };

  const checkAuthAndRedirect = async (): Promise<boolean> => {
    try {
      const isAuthenticated = await authService.isAuthenticated();
      if (!isAuthenticated) {
        // Don't redirect here, just return false
        return false;
      }
      return true;
    } catch (err) {
      console.error('Error checking authentication:', err);
      setError('Error checking authentication status.');
      return false;
    }
  };

  const sendMessage = useCallback(async (messageText: string) => {
    if (!messageText.trim()) {
      setError('Message cannot be empty.');
      return;
    }

    let tempUserMessage: Message | null = null;

    try {
      setIsLoading(true);
      setError(null);

      // Sanitize the message
      const sanitizedMessage = sanitizeMessageContent(messageText);

      // Create a temporary user message to show immediately
      tempUserMessage = {
        id: generateMessageId(),
        content: sanitizedMessage,
        role: 'user',
        timestamp: new Date(),
        status: 'pending',
        type: 'text',
        userId: await authService.getCurrentUserId() || 'unknown',
        conversationId: '', // Will be updated after receiving response
      };

      // Add user message to UI immediately
      setMessages(prev => [...prev, tempUserMessage!]);

      // Always try to use the real API, but check authentication status
      const response = await chatApi.sendMessage({
        message: sanitizedMessage,
        conversationId: getActiveConversationId(),
      });

      if ('success' in response && !response.success) {
        // Handle error response
        if ('errorCode' in response && (response.errorCode === 'UNAUTHORIZED' ||
            ('error' in response && typeof response.error === 'string' && response.error.toLowerCase().includes('401')))) {
          console.warn('Authentication failed, received 401 from server');

          // Even if the local auth check passed, the server rejected the token
          // This could mean the token expired or is invalid
          setError('Authentication token is invalid. Please sign in again.');
          setMessages(prev => prev.filter(msg => msg.id !== tempUserMessage!.id)); // Remove temp message
          return;
        }
        throw new Error('error' in response ? response.error : 'Failed to send message');
      }

      if ('session_id' in response && response.response) {
        // Update the temporary user message with the confirmed one
        setMessages(prev =>
          prev.map(msg =>
            msg.id === tempUserMessage!.id
              ? { ...msg, status: 'sent' } as Message
              : msg
          )
        );

        // Get user ID for the message
        const userId = await authService.getCurrentUserId() || 'unknown';

        // Add the assistant's response from the backend
        const assistantMessage: Message = {
          id: `resp_${Date.now()}`,
          content: response.response,
          role: 'assistant' as const,
          timestamp: new Date(response.timestamp || Date.now()),
          status: 'sent',
          type: 'response',
          userId: userId,
          conversationId: response.session_id || getActiveConversationId() || ''
        };

        setMessages(prev => [...prev, assistantMessage]);
      } else {
        // If response doesn't have expected structure, remove temp message and show error
        setMessages(prev => prev.filter(msg => msg.id !== tempUserMessage!.id));
        throw new Error('Invalid response from server');
      }
    } catch (err) {
      console.error('Error sending message:', err);
      setError(err instanceof Error ? err.message : 'Failed to send message. Please try again.');

      // Remove the temporary message if it was created and there was an error
      if (tempUserMessage) {
        setMessages(prev => prev.filter(msg => msg.id !== tempUserMessage!.id));
      }
    } finally {
      setIsLoading(false);
      setCurrentInput('');
    }
  }, []);

  const getActiveConversationId = (): string | undefined => {
    // Find the most recent conversation based on messages
    if (messages.length > 0) {
      return messages[messages.length - 1].conversationId || undefined;
    }
    return undefined;
  };

  const clearMessages = useCallback(() => {
    setMessages([]);
    setError(null);
  }, []);

  const reconnect = useCallback(() => {
    setIsLoading(false);
    setError(null);
  }, []);

  return {
    messages,
    isLoading,
    currentInput,
    error,
    sendMessage,
    setCurrentInput,
    clearMessages,
    reconnect,
    checkAuthAndRedirect,
  };
};