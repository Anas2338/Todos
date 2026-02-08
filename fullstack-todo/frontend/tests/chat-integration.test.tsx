// Simple integration test for chat functionality
import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ChatProvider } from '@/providers/ChatProvider';
import ChatInterface from '@/components/chatbot/ChatInterface';

describe('Chat Integration', () => {
  it('renders chat interface correctly', () => {
    render(
      <ChatProvider>
        <ChatInterface />
      </ChatProvider>
    );

    expect(screen.getByText('Todo Assistant')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Ask me to manage your tasks...')).toBeInTheDocument();
  });

  it('allows user to type and submit messages', async () => {
    render(
      <ChatProvider>
        <ChatInterface />
      </ChatProvider>
    );

    const input = screen.getByPlaceholderText('Ask me to manage your tasks...');
    const sendButton = screen.getByRole('button', { name: '' }); // The send button with SVG icon

    fireEvent.change(input, { target: { value: 'Test message' } });
    fireEvent.click(sendButton);

    // We can't actually test the API call in this simple test
    // But we can verify the input was cleared after submission
    await waitFor(() => {
      expect(input).toHaveValue('');
    });
  });

  it('displays welcome message when no messages exist', () => {
    render(
      <ChatProvider>
        <ChatInterface />
      </ChatProvider>
    );

    expect(screen.getByText('Hello! I\'m your Todo Assistant.')).toBeInTheDocument();
  });
});