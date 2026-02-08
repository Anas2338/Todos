'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/input';
import { validateEmail } from '@/lib/utils/validation';

interface FormData {
  email: string;
}

export default function ForgotPasswordForm() {
  const [formData, setFormData] = useState<FormData>({ email: '' });
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState<{ email?: string }>({});

  const router = useRouter();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));

    // Clear field-specific error when user starts typing
    if (errors[name as keyof typeof errors]) {
      setErrors(prev => ({ ...prev, [name]: undefined }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);
    setErrors({});

    // Validate email
    if (!formData.email) {
      setErrors({ email: 'Email is required' });
      return;
    }

    if (!validateEmail(formData.email)) {
      setErrors({ email: 'Please enter a valid email address' });
      return;
    }

    setLoading(true);

    try {
      // Call the API to send password reset email
      const response = await fetch('/api/auth/forgot-password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: formData.email }),
      });

      if (response.ok) {
        setSuccess('Password reset link has been sent to your email address.');
        setFormData({ email: '' });
      } else {
        const data = await response.json();
        setError(data.message || 'Failed to send password reset email. Please try again.');
      }
    } catch (err) {
      setError('An error occurred. Please try again.');
      console.error('Forgot password error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
      {error && (
        <div className="rounded-md bg-red-50 p-4">
          <div className="text-sm text-red-700">{error}</div>
        </div>
      )}

      {success && (
        <div className="rounded-md bg-green-50 p-4">
          <div className="text-sm text-green-700">{success}</div>
        </div>
      )}

      <div className="rounded-md shadow-sm -space-y-px">
        <div>
          <Input
            id="email"
            name="email"
            type="email"
            autoComplete="email"
            required
            placeholder="Email address"
            value={formData.email}
            onChange={handleChange}
            error={errors.email}
          />
        </div>
      </div>

      <div>
        <Button
          type="submit"
          disabled={loading}
          className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
        >
          {loading ? 'Sending...' : 'Send Reset Link'}
        </Button>
      </div>

      <div className="text-center text-sm text-gray-600">
        <button
          type="button"
          onClick={() => router.push('/login')}
          className="font-medium text-indigo-600 hover:text-indigo-500"
        >
          Back to login
        </button>
      </div>
    </form>
  );
}