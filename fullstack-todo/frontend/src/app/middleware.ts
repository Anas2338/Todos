import { NextRequest, NextResponse } from 'next/server';

// This function protects routes that require authentication
export function middleware(request: NextRequest) {
  // Define protected routes that require authentication
  const protectedPaths = [
    '/dashboard',
    '/tasks',
  ];

  const isProtectedPath = protectedPaths.some(path =>
    request.nextUrl.pathname.startsWith(path)
  );

  // Check for auth token in cookies (the auth system stores it as 'auth-token')
  const authTokenCookie = request.cookies.get('auth-token');

  // Also check for the original better-auth-session cookie for compatibility
  const sessionCookie = request.cookies.get('better-auth-session');

  // If user is accessing a protected route without a session, redirect to login
  if (isProtectedPath && !authTokenCookie && !sessionCookie) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // Allow the request to proceed
  return NextResponse.next();
}

// Define which paths the middleware should run on
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};