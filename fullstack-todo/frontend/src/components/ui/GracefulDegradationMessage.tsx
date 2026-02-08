import React from 'react';
import Button from './button';

interface GracefulDegradationMessageProps {
  title?: string;
  message?: string;
  onRetry?: () => void;
  onOfflineMode?: () => void;
  showActions?: boolean;
}

const GracefulDegradationMessage: React.FC<GracefulDegradationMessageProps> = ({
  title = 'Service Temporarily Unavailable',
  message = 'We\'re experiencing some technical difficulties. Please try again in a moment.',
  onRetry,
  onOfflineMode,
  showActions = true,
}) => {
  return (
    <div className="flex flex-col items-center justify-center p-8 bg-white rounded-lg shadow-md max-w-md mx-auto text-center">
      <div className="bg-yellow-100 p-4 rounded-full mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-yellow-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
      </div>

      <h2 className="text-xl font-semibold text-gray-800 mb-2">{title}</h2>
      <p className="text-gray-600 mb-6">{message}</p>

      {showActions && (
        <div className="flex flex-col sm:flex-row gap-3 w-full max-w-xs">
          {onRetry && (
            <Button
              onClick={onRetry}
              variant="primary"
              className="flex-1"
            >
              Retry Connection
            </Button>
          )}
          {onOfflineMode && (
            <Button
              onClick={onOfflineMode}
              variant="outline"
              className="flex-1"
            >
              Use Offline Mode
            </Button>
          )}
        </div>
      )}
    </div>
  );
};

export default GracefulDegradationMessage;