import { NextRequest, NextResponse } from 'next/server';

// Handler for reset password request
export async function POST(request: NextRequest) {
  try {
    const { token, newPassword } = await request.json();

    // Forward the request to the backend service
    const backendResponse = await fetch(`${process.env.BACKEND_API_URL || 'http://localhost:8000'}/auth/reset-password`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ token, newPassword }),
    });

    if (backendResponse.ok) {
      const result = await backendResponse.json();
      return NextResponse.json(result, { status: 200 });
    } else {
      const errorResult = await backendResponse.json();
      return NextResponse.json(errorResult, { status: backendResponse.status });
    }
  } catch (error) {
    console.error('Reset password error:', error);
    return NextResponse.json({ message: 'Failed to reset password' }, { status: 500 });
  }
}