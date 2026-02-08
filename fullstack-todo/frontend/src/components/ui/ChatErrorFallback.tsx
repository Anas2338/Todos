import React from 'react';
import Button from './button';

interface ChatErrorFallbackProps {
  error: Error;
  onReset?: () => void;
}

const ChatErrorFallback: React.FC<ChatErrorFallbackProps> = ({ error, onReset }) => {
  return (
    <div className="flex flex-col items-center justify-center p-8 bg-white rounded-lg shadow-md max-w-md mx-auto">
      <div className="bg-red-100 p-3 rounded-full mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
      </div>

      <h2 className="text-xl font-semibold text-gray-800 mb-2">Chat Interface Error</h2>
      <p className="text-gray-600 text-center mb-4">
        The chat interface encountered an error and needs to be refreshed.
      </p>

      <details className="w-full mb-4">
        <summary className="text-left text-sm text-gray-500 cursor-pointer hover:text-gray-700">
          Show error details
        </summary>
        <pre className="mt-2 p-2 bg-gray-100 text-xs text-red-700 rounded overflow-x-auto">
          {error.stack || error.message}
        </pre>
      </details>

      <div className="flex gap-2">
        {onReset && (
          <Button
            onClick={onReset}
            variant="primary"
          >
            Reset Chat Interface
          </Button>
        )}
        <Button
          variant="outline"
          onClick={() => window.location.reload()}
        >
          Reload Page
        </Button>
      </div>
    </div>
  );
};

export default ChatErrorFallback;