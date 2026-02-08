'use client';

import { useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/input';
import { validatePassword } from '@/lib/utils/validation';

interface FormData {
  password: string;
  confirmPassword: string;
}

export default function PasswordResetForm() {
  const [formData, setFormData] = useState<FormData>({ password: '', confirmPassword: '' });
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState<{ password?: string; confirmPassword?: string }>({});

  const router = useRouter();
  const searchParams = useSearchParams();
  const token = searchParams.get('token');

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

    // Validate passwords
    if (!formData.password) {
      setErrors({ password: 'Password is required' });
      return;
    }

    if (!validatePassword(formData.password)) {
      setErrors({ password: 'Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number' });
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setErrors({ confirmPassword: 'Passwords do not match' });
      return;
    }

    if (!token) {
      setError('Invalid reset token. Please try resetting your password again.');
      return;
    }

    setLoading(true);

    try {
      // Call the API to reset password
      const response = await fetch('/api/auth/reset-password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          token,
          newPassword: formData.password,
        }),
      });

      if (response.ok) {
        setSuccess('Your password has been reset successfully. Redirecting to login...');

        // Redirect to login after a short delay
        setTimeout(() => {
          router.push('/login');
        }, 2000);
      } else {
        const data = await response.json();
        setError(data.message || 'Failed to reset password. Please try again.');
      }
    } catch (err) {
      setError('An error occurred. Please try again.');
      console.error('Password reset error:', err);
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

      <input type="hidden" name="token" value={token || ''} />

      <div className="rounded-md shadow-sm -space-y-px">
        <div>
          <Input
            id="password"
            name="password"
            type="password"
            autoComplete="new-password"
            required
            placeholder="New password"
            value={formData.password}
            onChange={handleChange}
            error={errors.password}
            showPasswordToggle={true}
          />
        </div>
        <div className="mt-4">
          <Input
            id="confirmPassword"
            name="confirmPassword"
            type="password"
            autoComplete="new-password"
            required
            placeholder="Confirm new password"
            value={formData.confirmPassword}
            onChange={handleChange}
            error={errors.confirmPassword}
            showPasswordToggle={true}
          />
        </div>
      </div>

      <div>
        <Button
          type="submit"
          disabled={loading}
          className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
        >
          {loading ? 'Resetting...' : 'Reset Password'}
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