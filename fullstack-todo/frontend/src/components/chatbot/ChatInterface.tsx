import React from 'react';
import { useChatBot } from '@/hooks/useChatBot';
import { Message } from '@/types/chat';

interface ChatInterfaceProps {
  onToggleChat?: () => void;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({ onToggleChat }) => {
  const {
    messages,
    isLoading,
    currentInput,
    error,
    sendMessage,
    setCurrentInput,
    clearMessages
  } = useChatBot();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (currentInput.trim() && !isLoading) {
      await sendMessage(currentInput);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setCurrentInput(e.target.value);
  };

  return (
    <div className="flex flex-col h-full bg-white rounded-lg shadow-md overflow-hidden">
      {/* Chat Header */}
      <div className="bg-gray-800 text-white p-3 flex justify-between items-center">
        <h3 className="font-medium">Todo Assistant</h3>
        <button
          onClick={onToggleChat}
          className="text-gray-300 hover:text-white"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
          </svg>
        </button>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 bg-gray-50 min-h-[300px]">
        {error && (
          <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-md">
            {error}
          </div>
        )}

        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-gray-500">
            <div className="text-center">
              <p>Hello! I'm your Todo Assistant.</p>
              <p className="mt-2">You can ask me to:</p>
              <ul className="mt-2 grid grid-cols-2 gap-2 text-sm">
                <li className="bg-blue-100 p-2 rounded">• Add tasks</li>
                <li className="bg-green-100 p-2 rounded">• List tasks</li>
                <li className="bg-yellow-100 p-2 rounded">• Update tasks</li>
                <li className="bg-purple-100 p-2 rounded">• Complete tasks</li>
              </ul>
              <p className="mt-4 text-xs italic">Try: "Add a task to buy groceries"</p>
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
                    <span className="mr-2">Thinking...</span>
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

      {/* Input Area */}
      <div className="border-t border-gray-200 p-3 bg-white">
        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            type="text"
            value={currentInput}
            onChange={handleInputChange}
            placeholder="Ask me to manage your tasks..."
            className="flex-1 border border-gray-300 rounded-full px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!currentInput.trim() || isLoading}
            className={`rounded-full h-10 w-10 flex items-center justify-center ${
              !currentInput.trim() || isLoading
                ? 'bg-gray-300 cursor-not-allowed'
                : 'bg-blue-500 hover:bg-blue-600'
            }`}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-white" viewBox="0 0 20 20" fill="currentColor">
              <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
            </svg>
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatInterface;