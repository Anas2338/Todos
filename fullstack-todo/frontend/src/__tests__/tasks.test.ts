// Unit tests for task CRUD operations

import { validateTaskTitle, validateTaskDescription } from '@/lib/utils/validation';

describe('Task validation functions', () => {
  describe('validateTaskTitle', () => {
    test('should return true for title with 1-100 characters', () => {
      expect(validateTaskTitle('A')).toBe(true);
      expect(validateTaskTitle('A'.repeat(50))).toBe(true);
      expect(validateTaskTitle('A'.repeat(100))).toBe(true);
    });

    test('should return false for title with 0 or more than 100 characters', () => {
      expect(validateTaskTitle('')).toBe(false);
      expect(validateTaskTitle('A'.repeat(101))).toBe(false);
    });
  });

  describe('validateTaskDescription', () => {
    test('should return true for description with 0-1000 characters', () => {
      expect(validateTaskDescription('')).toBe(true);
      expect(validateTaskDescription('A'.repeat(500))).toBe(true);
      expect(validateTaskDescription('A'.repeat(1000))).toBe(true);
    });

    test('should return false for description with more than 1000 characters', () => {
      expect(validateTaskDescription('A'.repeat(1001))).toBe(false);
    });
  });
});