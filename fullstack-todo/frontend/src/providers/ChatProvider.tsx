'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { ChatState, Conversation, Message } from '@/types/chat';
import { chatApi } from '@/services/chatApi';
import { authService } from '@/services/authService';

interface ChatContextType {
  session: ChatState;
  conversations: Conversation[];
  activeConversation: Conversation | null;
  sendMessage: (message: string) => Promise<void>;
  startNewConversation: () => Promise<void>;
  loadConversation: (conversationId: string) => Promise<void>;
  loadConversations: () => Promise<void>;
  closeChat: () => void;
  openChat: () => void;
  setError: (error: string | null) => void;
  clearError: () => void;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

interface ChatProviderProps {
  children: ReactNode;
}

export const ChatProvider: React.FC<ChatProviderProps> = ({ children }) => {
  const [session, setSession] = useState<ChatState>({
    messages: [],
    isLoading: false,
    currentInput: '',
    error: null,
    streamingResponse: null,
    toolCallStatus: null,
    isConnected: true,
    sessionId: '',
  });

  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConversation, setActiveConversation] = useState<Conversation | null>(null);

  // Initialize chat session
  useEffect(() => {
    initializeChat();
  }, []);

  const initializeChat = async () => {
    try {
      // Check authentication
      const isAuthenticated = await authService.isAuthenticated();

      // Set up initial session regardless of authentication status
      // The chat can still function, but with limited capabilities when not authenticated
      setSession(prev => ({
        ...prev,
        isConnected: isAuthenticated, // Only mark as connected if authenticated
        sessionId: `session_${Date.now()}`,
      }));

      // Only load existing conversations if authenticated
      if (isAuthenticated) {
        await loadConversations();
      } else {
        console.warn('User not authenticated, skipping conversation load during initialization');
      }
    } catch (error) {
      console.error('Error initializing chat:', error);
      // Still initialize with basic session even if there are issues
      setSession(prev => ({
        ...prev,
        isConnected: false,
        sessionId: `session_${Date.now()}`,
      }));
    }
  };

  const sendMessage = async (message: string) => {
    if (!message.trim()) return;

    // Check authentication
    const isAuthenticated = await authService.isAuthenticated();
    if (!isAuthenticated) {
      setSession(prev => ({
        ...prev,
        error: 'User not authenticated. Please log in to send messages.',
      }));
      return;
    }

    try {
      setSession(prev => ({
        ...prev,
        isLoading: true,
        error: null,
        currentInput: '',
      }));

      // Add user message to UI immediately
      const userMessage: Message = {
        id: `temp-${Date.now()}`,
        content: message,
        role: 'user',
        timestamp: new Date(),
        status: 'pending',
        type: 'text',
        userId: await authService.getCurrentUserId() || 'unknown',
        conversationId: activeConversation?.id || '',
      };

      setSession(prev => ({
        ...prev,
        messages: [...prev.messages, userMessage],
      }));

      // Send message to backend
      const response = await chatApi.sendMessage({
        message,
        conversationId: activeConversation?.id,
      });

      // Check if the response indicates an authentication error
      if ('error' in response && (response.errorCode === 'UNAUTHORIZED' || response.error.toLowerCase().includes('401') || response.error.toLowerCase().includes('unauthorized'))) {
        setSession(prev => ({
          ...prev,
          error: 'Authentication required. Please log in to send messages.',
          isLoading: false,
        }));
        return;
      }

      if ('success' in response && !response.success) {
        throw new Error('error' in response ? response.error : 'Failed to send message');
      }

      if ('session_id' in response && response.response) {
        // Update active conversation if needed
        if (response.session_id && (!activeConversation || activeConversation.id !== response.session_id)) {
          const newConversation = {
            id: response.session_id,
            userId: await authService.getCurrentUserId() || 'unknown',
            createdAt: new Date(),
            updatedAt: new Date(),
            isActive: true,
          };
          setActiveConversation(newConversation);

          // Add to conversations list if not already there
          if (!conversations.some(conv => conv.id === response.session_id)) {
            setConversations(prev => [...prev, newConversation]);
          }
        }

        // Add assistant message from response
        const userId = await authService.getCurrentUserId() || 'unknown';
        const assistantMessage: Message = {
          id: `resp_${Date.now()}`,
          content: response.response,
          role: 'assistant' as const,
          timestamp: new Date(response.timestamp || Date.now()),
          status: 'sent',
          type: 'response',
          userId: userId,
          conversationId: response.session_id || activeConversation?.id || ''
        };

        setSession(prev => ({
          ...prev,
          messages: [...prev.messages, assistantMessage],
        }));
      }
    } catch (error) {
      // Check if it's an authentication error
      if (error instanceof Error && (error.message.toLowerCase().includes('401') || error.message.toLowerCase().includes('unauthorized'))) {
        setSession(prev => ({
          ...prev,
          error: 'Authentication required. Please log in to send messages.',
          isLoading: false,
        }));
      } else {
        console.error('Error sending message:', error);
        setSession(prev => ({
          ...prev,
          error: 'Failed to send message. Please try again.',
          isLoading: false,
        }));
      }
    } finally {
      setSession(prev => ({
        ...prev,
        isLoading: false,
      }));
    }
  };

  const startNewConversation = async () => {
    // Check authentication first
    const isAuthenticated = await authService.isAuthenticated();
    if (!isAuthenticated) {
      setSession(prev => ({
        ...prev,
        error: 'User not authenticated. Please log in to start a new conversation.',
      }));
      return;
    }

    try {
      setSession(prev => ({
        ...prev,
        isLoading: true,
        error: null,
      }));

      const response = await chatApi.startConversation();

      // Check if the response indicates an authentication error
      if ('error' in response && typeof response.error === 'string' && (response.errorCode === 'UNAUTHORIZED' || response.error.toLowerCase().includes('401') || response.error.toLowerCase().includes('unauthorized'))) {
        setSession(prev => ({
          ...prev,
          error: 'Authentication required. Please log in to start a new conversation.',
          isLoading: false,
        }));
        return;
      }

      if ('success' in response && response.success && response.session_id) {
        const newConversation: Conversation = {
          id: response.session_id,
          userId: await authService.getCurrentUserId() || 'unknown',
          createdAt: new Date(),
          updatedAt: new Date(),
          isActive: true,
        };

        setActiveConversation(newConversation);
        setConversations(prev => [newConversation, ...prev]);

        // Clear current messages for new conversation
        setSession(prev => ({
          ...prev,
          messages: [],
        }));
      } else {
        const errorMessage = 'error' in response ? response.error : 'Failed to start new conversation';
        throw new Error(errorMessage);
      }
    } catch (error) {
      // Check if it's an authentication error
      if (error instanceof Error && (error.message.toLowerCase().includes('401') || error.message.toLowerCase().includes('unauthorized'))) {
        setSession(prev => ({
          ...prev,
          error: 'Authentication required. Please log in to start a new conversation.',
          isLoading: false,
        }));
      } else {
        console.error('Error starting new conversation:', error);
        setSession(prev => ({
          ...prev,
          error: 'Failed to start new conversation. Please try again.',
          isLoading: false,
        }));
      }
    } finally {
      setSession(prev => ({
        ...prev,
        isLoading: false,
      }));
    }
  };

  const loadConversation = async (conversationId: string) => {
    // Check authentication first
    const isAuthenticated = await authService.isAuthenticated();
    if (!isAuthenticated) {
      setSession(prev => ({
        ...prev,
        error: 'User not authenticated. Please log in to load conversations.',
        isLoading: false,
      }));
      return;
    }

    try {
      setSession(prev => ({
        ...prev,
        isLoading: true,
        error: null,
      }));

      const response = await chatApi.getHistory({ conversationId });

      // Check if the response indicates an authentication error
      if ('error' in response && (response.errorCode === 'UNAUTHORIZED' || response.error.toLowerCase().includes('401') || response.error.toLowerCase().includes('unauthorized'))) {
        setSession(prev => ({
          ...prev,
          error: 'Authentication required. Please log in to load conversations.',
          isLoading: false,
        }));
        return;
      }

      if ('messages' in response) {
        const fullConversation: Conversation = {
          id: conversationId,
          userId: await authService.getCurrentUserId() || 'unknown',
          createdAt: new Date(),
          updatedAt: new Date(),
          isActive: true,
        };

        setActiveConversation(fullConversation);

        // Update messages - map the response format to our internal format
        const userId = await authService.getCurrentUserId() || 'unknown';
        const mappedMessages = response.messages.map(msg => ({
          id: msg.id,
          content: msg.content,
          role: (msg.role === 'user' ? 'user' : 'assistant') as 'user' | 'assistant',
          timestamp: new Date(msg.timestamp),
          status: 'sent' as const,
          type: 'text' as const,
          userId: userId,
          conversationId: conversationId
        }));

        setSession(prev => ({
          ...prev,
          messages: mappedMessages,
        }));
      } else {
        throw new Error(response.error || 'Failed to load conversation');
      }
    } catch (error) {
      // Check if it's an authentication error
      if (error instanceof Error && (error.message.toLowerCase().includes('401') || error.message.toLowerCase().includes('unauthorized'))) {
        setSession(prev => ({
          ...prev,
          error: 'Authentication required. Please log in to load conversations.',
          isLoading: false,
        }));
      } else {
        console.error('Error loading conversation:', error);
        setSession(prev => ({
          ...prev,
          error: 'Failed to load conversation. Please try again.',
          isLoading: false,
        }));
      }
    } finally {
      setSession(prev => ({
        ...prev,
        isLoading: false,
      }));
    }
  };

  const loadConversations = async () => {
    try {
      // First check if user is authenticated
      const sessionCheck = await authService.getSession();
      if (!sessionCheck || !sessionCheck.user) {
        console.warn('User not authenticated, skipping conversation load');
        return;
      }

      setSession(prev => ({
        ...prev,
        isLoading: true,
      }));

      const response = await chatApi.getConversations();

      if ('sessions' in response) {
        const userId = sessionCheck.user.id || await authService.getCurrentUserId() || 'unknown';
        const convList = response.sessions.map(session => ({
          id: session.id,
          userId: userId,
          createdAt: new Date(session.created_at),
          updatedAt: new Date(session.updated_at),
          isActive: session.id === activeConversation?.id,
        }));

        setConversations(convList);
      } else if ('error' in response) {
        // Handle specific error responses
        if (response.errorCode === 'UNAUTHORIZED' || response.error.includes('401') || response.error.toLowerCase().includes('unauthorized')) {
          console.warn('Authentication failed when loading conversations, user may need to log in again');
          // Silently handle the auth error - don't set an error state that disrupts UX
          return;
        }
        // For other errors, log but don't throw to avoid UI disruption
        console.error('Error loading conversations:', response.error);
      }
    } catch (error) {
      // Check if it's an authentication error - silently handle auth errors
      if (error instanceof Error && (error.message.toLowerCase().includes('401') || error.message.toLowerCase().includes('unauthorized'))) {
        console.warn('Authentication failed when loading conversations, continuing without conversations');
        // Don't set error state for auth issues to avoid disrupting the UI
      } else {
        console.error('Error loading conversations:', error);
        // For other errors, log them but don't necessarily show to user
        console.error('Non-auth error loading conversations:', error);
      }
    } finally {
      setSession(prev => ({
        ...prev,
        isLoading: false,
      }));
    }
  };

  const openChat = () => {
    // In this context, opening chat might mean setting up the UI state
    // Since there's no specific isActive property in ChatState, we'll just ensure the session is connected
    setSession(prev => ({
      ...prev,
      isConnected: true,
    }));
  };

  const closeChat = () => {
    // In this context, closing chat might mean clearing the session
    // Since there's no specific isActive property in ChatState, we'll just clear the messages
    setSession(prev => ({
      ...prev,
      messages: [],
    }));
  };

  const setError = (error: string | null) => {
    setSession(prev => ({
      ...prev,
      error,
    }));
  };

  const clearError = () => {
    setSession(prev => ({
      ...prev,
      error: null,
    }));
  };

  const value = {
    session,
    conversations,
    activeConversation,
    sendMessage,
    startNewConversation,
    loadConversation,
    loadConversations,
    closeChat,
    openChat,
    setError,
    clearError,
  };

  return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>;
};

export const useChat = (): ChatContextType => {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};