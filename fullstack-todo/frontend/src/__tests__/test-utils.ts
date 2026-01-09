// Test utilities for the frontend application

import { render } from '@testing-library/react';
import { AuthProvider } from '@/components/providers/auth-provider';

// Mock Next.js router
export const mockRouter = {
  push: jest.fn(),
  replace: jest.fn(),
  reload: jest.fn(),
  back: jest.fn(),
  forward: jest.fn(),
  prefetch: jest.fn(),
  beforePopState: jest.fn(),
  events: {
    on: jest.fn(),
    off: jest.fn(),
    emit: jest.fn(),
  },
  isFallback: false,
  isLocaleDomain: false,
  isReady: true,
  query: {},
  asPath: '/',
  basePath: '',
  pathname: '/',
  route: '/',
};

// Wrapper component for testing with auth context
export const AllProviders = ({ children }: { children: React.ReactNode }) => {
  return (
    <AuthProvider>
      {children}
    </AuthProvider>
  );
};

// Custom render function with providers
export const customRender = (ui: React.ReactElement, options = {}) => {
  return render(ui, { wrapper: AllProviders, ...options });
};

// Re-export everything
export * from '@testing-library/react';

// Override render method
export { customRender as render };