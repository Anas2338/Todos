'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { betterAuthClient } from '@/lib/auth/client';

export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    const checkAuth = async () => {
      const session = await betterAuthClient.getSession();
      if (session) {
        // User is authenticated, redirect to dashboard
        router.push('/dashboard');
      } else {
        // User is not authenticated, redirect to login
        router.push('/login');
      }
    };

    checkAuth();
  }, [router]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Welcome to Todo App
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Redirecting...
          </p>
        </div>
      </div>
    </div>
  );
}