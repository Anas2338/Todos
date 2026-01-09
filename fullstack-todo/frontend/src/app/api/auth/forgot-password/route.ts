import { NextRequest, NextResponse } from 'next/server';

// Handler for forgot password request
export async function POST(request: NextRequest) {
  try {
    const { email } = await request.json();

    // Forward the request to the backend service
    const backendResponse = await fetch(`${process.env.BACKEND_API_URL || 'http://localhost:8000'}/auth/forgot-password`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email }),
    });

    if (backendResponse.ok) {
      const result = await backendResponse.json();
      return NextResponse.json(result, { status: 200 });
    } else {
      const errorResult = await backendResponse.json();
      return NextResponse.json(errorResult, { status: backendResponse.status });
    }
  } catch (error) {
    console.error('Forgot password error:', error);
    return NextResponse.json({ message: 'Failed to send reset email' }, { status: 500 });
  }
}