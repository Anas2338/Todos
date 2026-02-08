'use client';

import { useRouter } from 'next/navigation';
import Button from '@/components/ui/Button';

export default function NotFound() {
  const router = useRouter();

  const handleGoHome = () => {
    router.push('/');
  };

  return (
    <div className="min-h-screen bg-white flex flex-col">
      <main className="shrink-0">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-24">
          <div className="text-center">
            <p className="text-sm font-semibold text-indigo-600 uppercase tracking-wide">404 error</p>
            <h1 className="mt-2 text-4xl font-extrabold text-gray-900 sm:text-5xl">Page not found</h1>
            <p className="mt-2 text-base text-gray-500">
              Sorry, we couldn't find the page you're looking for.
            </p>
          </div>
          <div className="mt-12 flex justify-center">
            <Button onClick={handleGoHome}>
              Go back home
            </Button>
          </div>
        </div>
      </main>
    </div>
  );
}