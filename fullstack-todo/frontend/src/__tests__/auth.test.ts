// Unit tests for authentication flows

import { validateEmail, validatePassword } from '@/lib/utils/validation';

describe('Authentication validation functions', () => {
  describe('validateEmail', () => {
    test('should return true for valid email', () => {
      expect(validateEmail('test@example.com')).toBe(true);
      expect(validateEmail('user.name@domain.co.uk')).toBe(true);
    });

    test('should return false for invalid email', () => {
      expect(validateEmail('invalid-email')).toBe(false);
      expect(validateEmail('@example.com')).toBe(false);
      expect(validateEmail('test@')).toBe(false);
      expect(validateEmail('')).toBe(false);
    });
  });

  describe('validatePassword', () => {
    test('should return true for password with 8 or more characters', () => {
      expect(validatePassword('password')).toBe(true);
      expect(validatePassword('12345678')).toBe(true);
      expect(validatePassword('a'.repeat(10))).toBe(true);
    });

    test('should return false for password with less than 8 characters', () => {
      expect(validatePassword('pass')).toBe(false);
      expect(validatePassword('1234567')).toBe(false);
      expect(validatePassword('')).toBe(false);
    });
  });
});