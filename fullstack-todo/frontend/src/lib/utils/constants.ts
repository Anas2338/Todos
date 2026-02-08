// Application constants for the frontend application

// API endpoints
export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/api/auth/login',
    REGISTER: '/api/auth/register',
    LOGOUT: '/api/auth/logout',
    SESSION: '/api/auth/session',
  },
  TASKS: {
    BASE: '/api/{user_id}/tasks',
    GET_ALL: '/api/{user_id}/tasks',
    GET_BY_ID: '/api/{user_id}/tasks/{task_id}',
    CREATE: '/api/{user_id}/tasks',
    UPDATE: '/api/{user_id}/tasks/{task_id}',
    DELETE: '/api/{user_id}/tasks/{task_id}',
    TOGGLE_COMPLETE: '/api/{user_id}/tasks/{task_id}/complete',
  },
};

// Validation constants
export const VALIDATION = {
  EMAIL_REGEX: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  PASSWORD_MIN_LENGTH: 8,
  TASK_TITLE_MIN_LENGTH: 1,
  TASK_TITLE_MAX_LENGTH: 100,
  TASK_DESCRIPTION_MAX_LENGTH: 1000,
  NAME_MAX_LENGTH: 100,
};

// Error messages
export const ERROR_MESSAGES = {
  INVALID_EMAIL: 'Please enter a valid email address',
  INVALID_PASSWORD: 'Password must be at least 8 characters',
  INVALID_TASK_TITLE: 'Task title must be between 1 and 100 characters',
  INVALID_TASK_DESCRIPTION: 'Task description must be 1000 characters or less',
  INVALID_NAME: 'Name must be 100 characters or less',
  LOGIN_FAILED: 'Login failed. Please check your credentials.',
  REGISTRATION_FAILED: 'Registration failed. Please try again.',
  NETWORK_ERROR: 'Network error occurred. Please check your connection.',
  UNAUTHORIZED: 'Unauthorized access. Please log in.',
};

// Storage keys
export const STORAGE_KEYS = {
  AUTH_TOKEN: 'auth-token',
  USER_DATA: 'user-data',
  REFRESH_TOKEN: 'refresh-token',
};

// Route paths
export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  REGISTER: '/register',
  DASHBOARD: '/dashboard',
  TASKS: '/tasks',
  TASK_DETAIL: (id: string) => `/tasks/${id}`,
  TASK_EDIT: (id: string) => `/tasks/${id}/edit`,
  TASK_NEW: '/tasks/new',
};

// Default values
export const DEFAULTS = {
  PAGE_SIZE: 20,
  DEBOUNCE_DELAY: 300,
  REQUEST_TIMEOUT: 10000,
};