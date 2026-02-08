import React, { useState, useEffect, useRef } from 'react';
import { useChatBot } from '@/hooks/useChatBot';
import { Message } from '@/types/chat';
import { authService } from '@/services/authService';

interface ChatModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const ChatModal: React.FC<ChatModalProps> = ({ isOpen, onClose }) => {
  const {
    messages,
    isLoading,
    currentInput,
    error,
    sendMessage,
    setCurrentInput,
    clearMessages,
    checkAuthAndRedirect
  } = useChatBot();

  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom of messages when they change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (currentInput.trim() && !isLoading) {
      await sendMessage(currentInput);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setCurrentInput(e.target.value);
  };

  // Check auth when modal opens
  useEffect(() => {
    if (isOpen) {
      checkAuthAndRedirect();
    }
  }, [isOpen]);

  if (!isOpen) {
    return null;
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-md h-[600px] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b">
          <h2 className="text-lg font-semibold">Chat with Todo Assistant</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 focus:outline-none"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Messages Container */}
        <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
          {error && (
            <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-md">
              {error}
            </div>
          )}

          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-gray-500">
              <p>Start a conversation with the Todo Assistant!</p>
              <p className="mt-2 text-sm">Try commands like:</p>
              <ul className="mt-2 text-sm list-disc pl-5 space-y-1">
                <li>Add a task to buy groceries</li>
                <li>Show me my tasks for today</li>
                <li>Mark task "Buy milk" as complete</li>
              </ul>
            </div>
          ) : (
            <div className="space-y-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${
                    message.role === 'user' ? 'justify-end' : 'justify-start'
                  }`}
                >
                  <div
                    className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                      message.role === 'user'
                        ? 'bg-blue-500 text-white'
                        : 'bg-gray-200 text-gray-800'
                    }`}
                  >
                    <div className="whitespace-pre-wrap">{message.content}</div>
                    <div className="text-xs mt-1 opacity-70">
                      {new Date(message.timestamp).toLocaleTimeString([], {
                        hour: '2-digit',
                        minute: '2-digit',
                      })}
                    </div>
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-gray-200 text-gray-800 max-w-xs px-4 py-2 rounded-lg">
                    <div className="flex space-x-2">
                      <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-75"></div>
                      <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-150"></div>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="border-t p-4 bg-white">
          <form onSubmit={handleSubmit} className="flex gap-2">
            <input
              type="text"
              value={currentInput}
              onChange={handleInputChange}
              placeholder="Type your message..."
              className="flex-1 border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={!currentInput.trim() || isLoading}
              className={`px-4 py-2 rounded-md text-white ${
                !currentInput.trim() || isLoading
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-blue-500 hover:bg-blue-600'
              }`}
            >
              Send
            </button>
          </form>
          <div className="mt-2 text-xs text-gray-500 text-center">
            Powered by AI - Responses may vary
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatModal;