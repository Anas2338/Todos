'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/use-auth';
import { validateRegistrationForm } from '@/lib/utils/validation';
import Button from '@/components/ui/button';
import Input from '@/components/ui/input';

interface FormData {
  email: string;
  password: string;
  name?: string;
}

export default function SignUpForm() {
  const [formData, setFormData] = useState<FormData>({ email: '', password: '', name: '' });
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState<{ email?: string; password?: string; name?: string }>({});

  const { register } = useAuth();
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
    setErrors({});

    // Validate form
    const validation = validateRegistrationForm(formData.email, formData.password, formData.name);
    if (!validation.isValid) {
      const newErrors: { email?: string; password?: string; name?: string } = {};
      validation.errors.forEach(err => {
        if (err.includes('email')) {
          newErrors.email = err;
        } else if (err.includes('Password')) {
          newErrors.password = err;
        } else if (err.includes('Name')) {
          newErrors.name = err;
        }
      });
      setErrors(newErrors);
      return;
    }

    setLoading(true);

    try {
      await register(formData.email, formData.password, formData.name);
    } catch (err) {
      setError('Registration failed. Please try again.');
      console.error('Registration error:', err);
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
      <input type="hidden" name="remember" defaultValue="true" />
      <div className="rounded-md shadow-sm -space-y-px">
        <div>
          <Input
            id="name"
            name="name"
            type="text"
            autoComplete="name"
            placeholder="Full name (optional)"
            value={formData.name || ''}
            onChange={handleChange}
            error={errors.name}
          />
        </div>
        <div className="mt-4">
          <Input
            id="email-address"
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
        <div className="mt-4">
          <Input
            id="password"
            name="password"
            type="password"
            autoComplete="current-password"
            required
            placeholder="Password"
            value={formData.password}
            onChange={handleChange}
            error={errors.password}
            showPasswordToggle={true}
          />
        </div>
      </div>

      <div className="flex items-center">
        <input
          id="terms-and-privacy"
          name="terms-and-privacy"
          type="checkbox"
          className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
          required
        />
        <label htmlFor="terms-and-privacy" className="ml-2 block text-sm text-gray-900">
          I agree to the <a href="#" className="font-medium text-indigo-600 hover:text-indigo-500">Terms</a> and <a href="#" className="font-medium text-indigo-600 hover:text-indigo-500">Privacy Policy</a>
        </label>
      </div>

      <div>
        <Button
          type="submit"
          disabled={loading}
          className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
        >
          {loading ? 'Creating account...' : 'Create account'}
        </Button>
      </div>

      <div className="text-center text-sm text-gray-600">
        Already have an account?{' '}
        <a href="/login" className="font-medium text-indigo-600 hover:text-indigo-500">
          Sign in
        </a>
      </div>
    </form>
  );
}