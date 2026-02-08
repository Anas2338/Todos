// Type definitions for chat-related entities

export interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
  status: 'sent' | 'pending' | 'error' | 'streaming';
  type: 'text' | 'command' | 'response' | 'system' | 'tool_call' | 'tool_result';
  userId: string;
  conversationId: string;
  toolCalls?: Array<{
    id: string;
    type: string;
    function: {
      name: string;
      arguments: string;
    };
  }>;
  toolResults?: Array<{
    toolCallId: string;
    result: any;
  }>;
}

export interface Conversation {
  id: string;
  userId: string;
  createdAt: Date;
  updatedAt: Date;
  isActive: boolean;
}

export interface ChatState {
  messages: Message[];
  isLoading: boolean;
  currentInput: string;
  error: string | null;
  streamingResponse: string | null;
  toolCallStatus: string | null;
  isConnected: boolean;
  sessionId: string;
}

export interface ToolExecutionState {
  activeToolCalls: Array<{
    id: string;
    name: string;
    status: 'pending' | 'executing' | 'completed' | 'failed';
    startTime: Date;
    result?: any;
  }>;
  showNotifications: boolean;
}

// Chat request and response types
export interface ChatRequest {
  messages: Message[];
  userId: string;
  conversationId?: string;
  model?: string;
  stream?: boolean;
  maxTokens?: number;
  temperature?: number;
  tools?: Array<{
    type: string;
    function: {
      name: string;
      description?: string;
      parameters: any;
    };
  }>;
  tool_choice?: 'auto' | 'none' | 'required' | {
    type: 'function';
    function: {
      name: string;
    };
  };
}

export interface ChatResponse {
  choices: Array<{
    index: number;
    message: Message;
    finish_reason: 'stop' | 'length' | 'tool_calls' | 'content_filter' | 'function_call';
  }>;
  todosAffected?: any[];
  toolCalls?: Array<{
    id: string;
    type: 'function';
    function: {
      name: string;
      arguments: string;
    };
  }>;
  conversationId: string;
  id?: string;
  created?: number;
  model?: string;
  system_fingerprint?: string;
}