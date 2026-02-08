import React from 'react';
import { Message } from '@/types/chat';

interface MessageListProps {
  messages: Message[];
  isLoading?: boolean;
}

const MessageList: React.FC<MessageListProps> = ({ messages, isLoading = false }) => {
  return (
    <div className="flex-1 overflow-y-auto p-4 bg-gray-50 min-h-[300px]">
      {messages.length === 0 ? (
        <div className="flex flex-col items-center justify-center h-full text-gray-500">
          <div className="text-center">
            <p>No messages yet.</p>
            <p className="mt-2 text-sm">Start a conversation by sending a message!</p>
          </div>
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
                className={`max-w-xs md:max-w-md px-4 py-3 rounded-2xl ${
                  message.role === 'user'
                    ? 'bg-blue-500 text-white rounded-br-none'
                    : 'bg-white text-gray-800 border border-gray-200 rounded-bl-none'
                }`}
              >
                <div className="whitespace-pre-wrap break-words">{message.content}</div>
                <div className="text-xs mt-1 opacity-80 text-right">
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
              <div className="bg-white border border-gray-200 text-gray-800 max-w-xs px-4 py-3 rounded-2xl rounded-bl-none">
                <div className="flex items-center">
                  <span className="mr-2">Processing...</span>
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-75"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-150"></div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default MessageList;