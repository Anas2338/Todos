// Utility functions for chat functionality

import { Message, Conversation } from '@/types/chat';

/**
 * Format a date to a readable string
 */
export function formatDate(date: Date): string {
  return new Intl.DateTimeFormat('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    month: 'short',
    day: 'numeric',
  }).format(date);
}

/**
 * Validate if a message is valid
 */
export function isValidMessage(message: Message): boolean {
  return (
    !!message.id &&
    !!message.content &&
    message.content.trim().length > 0 &&
    !!message.role &&
    !!message.timestamp
  );
}

/**
 * Check if a message is from the user
 */
export function isUserMessage(message: Message): boolean {
  return message.role === 'user';
}

/**
 * Check if a message is from the assistant
 */
export function isAssistantMessage(message: Message): boolean {
  return message.role === 'assistant';
}

/**
 * Sanitize message content to prevent XSS
 */
export function sanitizeMessageContent(content: string): string {
  // Remove any potentially harmful HTML tags
  return content
    .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
    .replace(/<iframe\b[^<]*(?:(?!<\/iframe>)<[^<]*)*<\/iframe>/gi, '')
    .replace(/javascript:/gi, '')
    .trim();
}

/**
 * Generate a unique ID for a message
 */
export function generateMessageId(): string {
  return `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * Generate a unique ID for a conversation
 */
export function generateConversationId(): string {
  return `conv_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * Get the last message in a conversation
 */
export function getLastMessage(conversation: Conversation): Message | undefined {
  // The conversation from the API may not have messages directly
  // This function might not be applicable to the current Conversation type
  // Returning undefined as a safe fallback
  return undefined;
}

/**
 * Format messages for display
 */
export function formatMessageForDisplay(message: Message): string {
  // Simple formatting - in a real implementation, you might want to process markdown
  return message.content;
}

/**
 * Check if a conversation has expired based on retention policy
 * @param conversation The conversation to check
 * @param retentionDays Number of days to retain conversations (default 30)
 * @returns True if the conversation has expired
 */
export function hasConversationExpired(conversation: Conversation, retentionDays: number = 30): boolean {
  const now = new Date();
  const expirationDate = new Date(conversation.updatedAt);
  expirationDate.setDate(expirationDate.getDate() + retentionDays);
  return now > expirationDate;
}

/**
 * Filter out expired conversations
 * @param conversations Array of conversations to filter
 * @param retentionDays Number of days to retain conversations (default 30)
 * @returns Array of non-expired conversations
 */
export function filterExpiredConversations(conversations: Conversation[], retentionDays: number = 30): Conversation[] {
  return conversations.filter(conv => !hasConversationExpired(conv, retentionDays));
}

/**
 * Estimate reading time for a message in minutes
 */
export function estimateReadingTime(text: string): number {
  const wordsPerMinute = 200; // Average reading speed
  const wordCount = text.split(/\s+/).length;
  const minutes = Math.ceil(wordCount / wordsPerMinute);
  return Math.max(minutes, 1); // At least 1 minute
}

/**
 * Format conversation title based on first message or summary
 */
export function formatConversationTitle(conversation: Conversation, maxLength: number = 50): string {
  // The conversation type may not have messages directly
  // Using a fallback approach
  return `Conversation ${formatDate(conversation.createdAt)}`;
}