// Helper functions for the ChatKit integration

import { Message } from '@/types/chat';
import { Todo } from '@/types/todo';

/**
 * Generates a unique ID
 * @returns A random UUID string
 */
export const generateId = (): string => {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
};

/**
 * Formats a date to ISO string format
 * @param date The date to format
 * @returns Formatted date string
 */
export const formatDate = (date: Date): string => {
  return new Date(date).toISOString();
};

/**
 * Sanitizes user input to prevent injection attacks
 * @param input The input string to sanitize
 * @returns Sanitized string
 */
export const sanitizeInput = (input: string): string => {
  if (!input || typeof input !== 'string') {
    return '';
  }

  // Remove potentially dangerous characters and patterns
  return input
    .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
    .replace(/<iframe\b[^<]*(?:(?!<\/iframe>)<[^<]*)*<\/iframe>/gi, '')
    .replace(/javascript:/gi, '')
    .replace(/vbscript:/gi, '')
    .replace(/on\w+="[^"]*"/gi, '')
    .replace(/on\w+='[^']*'/gi, '')
    .replace(/<[^>]*>/g, '') // Remove all HTML tags
    .replace(/&lt;/g, '')
    .replace(/&gt;/g, '')
    .replace(/&amp;/g, '')
    .replace(/&quot;/g, '')
    .replace(/&#x?[\dA-Fa-f]+;/g, '') // Remove HTML entities
    .trim();
};

/**
 * Validates if a string is safe to use
 * @param input The input string to validate
 * @returns True if safe, false otherwise
 */
export const isSafeInput = (input: string): boolean => {
  if (!input || typeof input !== 'string') {
    return false;
  }

  // Check for potentially dangerous patterns
  const dangerousPatterns = [
    /<script/i,
    /javascript:/i,
    /vbscript:/i,
    /on\w+=/i,
    /<iframe/i,
    /<object/i,
    /<embed/i,
    /eval\(/i,
    /expression\(/i,
    /javascript:/i,
  ];

  for (const pattern of dangerousPatterns) {
    if (pattern.test(input)) {
      return false;
    }
  }

  return true;
};

/**
 * Validates if a message content is safe
 * @param content The message content to validate
 * @returns True if safe, false otherwise
 */
export const isSafeMessageContent = (content: string): boolean => {
  if (!content || typeof content !== 'string') {
    return false;
  }

  // Check length
  if (content.length > 2000) {
    return false;
  }

  // Check for dangerous patterns
  if (!isSafeInput(content)) {
    return false;
  }

  return true;
};

/**
 * Validates if a todo title is safe
 * @param title The todo title to validate
 * @returns True if safe, false otherwise
 */
export const isSafeTodoTitle = (title: string): boolean => {
  if (!title || typeof title !== 'string') {
    return false;
  }

  // Check length
  if (title.length < 1 || title.length > 255) {
    return false;
  }

  // Check for dangerous patterns
  if (!isSafeInput(title)) {
    return false;
  }

  return true;
};

/**
 * Validates if a message is valid
 * @param message The message to validate
 * @returns True if valid, false otherwise
 */
export const isValidMessage = (message: Message): boolean => {
  if (!message.content || message.content.length < 1 || message.content.length > 2000) {
    return false;
  }

  if (!['user', 'assistant'].includes(message.role)) {
    return false;
  }

  if (!['sent', 'pending', 'error', 'streaming'].includes(message.status)) {
    return false;
  }

  if (!['text', 'command', 'response', 'system', 'tool_call', 'tool_result'].includes(message.type)) {
    return false;
  }

  return true;
};

/**
 * Validates if a todo is valid
 * @param todo The todo to validate
 * @returns True if valid, false otherwise
 */
export const isValidTodo = (todo: Todo): boolean => {
  if (!todo.id || !todo.title) {
    return false;
  }

  if (todo.title.length < 1 || todo.title.length > 255) {
    return false;
  }

  if (typeof todo.completed !== 'boolean') {
    return false;
  }

  if (todo.priority && !['low', 'medium', 'high'].includes(todo.priority)) {
    return false;
  }

  return true;
};

/**
 * Debounces a function
 * @param func The function to debounce
 * @param delay The delay in milliseconds
 * @returns Debounced function
 */
export const debounce = <T extends (...args: any[]) => any>(
  func: T,
  delay: number
): ((...args: Parameters<T>) => void) => {
  let timeoutId: NodeJS.Timeout;
  return (...args: Parameters<T>) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
};

/**
 * Formats a timestamp for display
 * @param timestamp The timestamp to format
 * @returns Formatted time string
 */
export const formatTime = (timestamp: Date): string => {
  const date = new Date(timestamp);
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

/**
 * Formats a date for display
 * @param timestamp The timestamp to format
 * @returns Formatted date string
 */
export const formatDateDisplay = (timestamp: Date): string => {
  const date = new Date(timestamp);
  const today = new Date();
  const yesterday = new Date(today);
  yesterday.setDate(yesterday.getDate() - 1);

  if (date.toDateString() === today.toDateString()) {
    return `Today at ${formatTime(date)}`;
  } else if (date.toDateString() === yesterday.toDateString()) {
    return `Yesterday at ${formatTime(date)}`;
  } else {
    return date.toLocaleDateString();
  }
};

/**
 * Checks if a value is a valid email
 * @param email The email to validate
 * @returns True if valid email, false otherwise
 */
export const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

/**
 * Capitalizes the first letter of a string
 * @param str The string to capitalize
 * @returns Capitalized string
 */
export const capitalize = (str: string): string => {
  if (!str) return str;
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
};

/**
 * Deep clones an object
 * @param obj The object to clone
 * @returns Cloned object
 */
export const deepClone = <T>(obj: T): T => {
  if (obj === null || typeof obj !== 'object') {
    return obj;
  }

  if (obj instanceof Date) {
    return new Date(obj.getTime()) as any;
  }

  if (Array.isArray(obj)) {
    return obj.map(item => deepClone(item)) as any;
  }

  const clonedObj: any = {};
  Object.keys(obj).forEach(key => {
    clonedObj[key] = deepClone((obj as any)[key]);
  });

  return clonedObj;
};

/**
 * Compares two objects for equality
 * @param obj1 First object
 * @param obj2 Second object
 * @returns True if objects are equal, false otherwise
 */
export const isEqual = (obj1: any, obj2: any): boolean => {
  if (obj1 === obj2) return true;
  if (obj1 == null || obj2 == null) return false;
  if (typeof obj1 !== 'object' || typeof obj2 !== 'object') return obj1 === obj2;

  const keys1 = Object.keys(obj1);
  const keys2 = Object.keys(obj2);

  if (keys1.length !== keys2.length) return false;

  for (const key of keys1) {
    if (!keys2.includes(key)) return false;
    if (!isEqual(obj1[key], obj2[key])) return false;
  }

  return true;
};

/**
 * Formats error message for display
 * @param error The error object
 * @returns Formatted error message
 */
export const formatErrorMessage = (error: any): string => {
  if (error instanceof Error) {
    return error.message;
  }
  if (typeof error === 'string') {
    return error;
  }
  if (error && typeof error === 'object' && error.message) {
    return error.message;
  }
  return 'An unknown error occurred';
};

/**
 * Waits for a specified duration
 * @param ms Number of milliseconds to wait
 * @returns Promise that resolves after the specified time
 */
export const sleep = (ms: number): Promise<void> => {
  return new Promise(resolve => setTimeout(resolve, ms));
};

/**
 * Generates a random color
 * @returns Random hex color string
 */
export const getRandomColor = (): string => {
  const letters = '0123456789ABCDEF';
  let color = '#';
  for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
};