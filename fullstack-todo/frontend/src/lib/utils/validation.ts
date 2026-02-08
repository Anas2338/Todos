// Form validation utilities for the frontend application

// Validate email format
export function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

// Validate password strength
export function validatePassword(password: string): boolean {
  // At least 8 characters
  return password.length >= 8;
}

// Validate task title (1-100 characters)
export function validateTaskTitle(title: string): boolean {
  return title.length >= 1 && title.length <= 100;
}

// Validate task description (0-1000 characters)
export function validateTaskDescription(description: string): boolean {
  return description.length <= 1000;
}

// Validate required field
export function validateRequired(value: string): boolean {
  return value.trim().length > 0;
}

// Validate field length
export function validateLength(value: string, min: number, max: number): boolean {
  return value.length >= min && value.length <= max;
}

// Validation result type
export interface ValidationResult {
  isValid: boolean;
  errors: string[];
}

// Validate login form
export function validateLoginForm(email: string, password: string): ValidationResult {
  const errors: string[] = [];

  if (!validateEmail(email)) {
    errors.push('Please enter a valid email address');
  }

  if (!validatePassword(password)) {
    errors.push('Password must be at least 8 characters');
  }

  return {
    isValid: errors.length === 0,
    errors,
  };
}

// Validate registration form
export function validateRegistrationForm(
  email: string,
  password: string,
  name?: string
): ValidationResult {
  const errors: string[] = [];

  if (!validateEmail(email)) {
    errors.push('Please enter a valid email address');
  }

  if (!validatePassword(password)) {
    errors.push('Password must be at least 8 characters');
  }

  if (name && name.length > 100) {
    errors.push('Name must be 100 characters or less');
  }

  return {
    isValid: errors.length === 0,
    errors,
  };
}

// Validate task form
export function validateTaskForm(title: string, description?: string): ValidationResult {
  const errors: string[] = [];

  if (!validateTaskTitle(title)) {
    errors.push('Task title must be between 1 and 100 characters');
  }

  if (description && !validateTaskDescription(description)) {
    errors.push('Task description must be 1000 characters or less');
  }

  return {
    isValid: errors.length === 0,
    errors,
  };
}