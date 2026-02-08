// Constants for the ChatKit integration

// API endpoints
export const API_ENDPOINTS = {
  CHAT: '/api/chat',
  AUTH: '/api/auth',
  TODO: '/api/todos',
  CONVERSATIONS: '/api/conversations',
};

// Configuration
export const CONFIG = {
  MAX_MESSAGE_LENGTH: 2000,
  MIN_MESSAGE_LENGTH: 1,
  DEBOUNCE_DELAY: 300,
  RETRY_ATTEMPTS: 3,
  RETRY_DELAY: 1000,
  STREAMING_TIMEOUT: 30000,
  WEBSOCKET_RECONNECT_INTERVAL: 5000,
  WS_BASE_URL: typeof window !== 'undefined'
    ? `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${window.location.host}`
    : 'ws://localhost:3000',
};

// Message types
export const MESSAGE_TYPES = {
  TEXT: 'text',
  COMMAND: 'command',
  RESPONSE: 'response',
  SYSTEM: 'system',
  TOOL_CALL: 'tool_call',
  TOOL_RESULT: 'tool_result',
};

// Message statuses
export const MESSAGE_STATUSES = {
  SENT: 'sent',
  PENDING: 'pending',
  ERROR: 'error',
  STREAMING: 'streaming',
};

// Roles
export const ROLES = {
  USER: 'user',
  ASSISTANT: 'assistant',
};

// Priorities
export const PRIORITIES = {
  LOW: 'low',
  MEDIUM: 'medium',
  HIGH: 'high',
};

// Events
export const EVENTS = {
  MESSAGE_SENT: 'message_sent',
  MESSAGE_RECEIVED: 'message_received',
  CONNECTION_OPENED: 'connection_opened',
  CONNECTION_CLOSED: 'connection_closed',
  ERROR_OCCURRED: 'error_occurred',
  TOOL_STARTED: 'tool_started',
  TOOL_COMPLETED: 'tool_completed',
};

// Storage keys
export const STORAGE_KEYS = {
  AUTH_TOKEN: 'auth_token',
  REFRESH_TOKEN: 'refresh_token',
  USER_PREFERENCES: 'user_preferences',
  CONVERSATION_HISTORY: 'conversation_history',
};

// Error messages
export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Network error occurred',
  AUTH_ERROR: 'Authentication error',
  INVALID_INPUT: 'Invalid input provided',
  SERVER_ERROR: 'Server error occurred',
  TIMEOUT_ERROR: 'Request timed out',
};

// UI constants
export const UI_CONSTANTS = {
  LOADING_INDICATOR_DELAY: 500, // Delay before showing loading indicator
  TOAST_DURATION: 5000, // Duration for toast notifications in ms
  ANIMATION_DURATION: 300, // Duration for UI animations in ms
};