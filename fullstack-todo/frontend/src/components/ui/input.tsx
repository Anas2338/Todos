import React, { useState, InputHTMLAttributes, TextareaHTMLAttributes } from 'react';

interface BaseInputProps {
  label?: string;
  error?: string;
  helperText?: string;
  className?: string;
  showPasswordToggle?: boolean;
  as?: 'input' | 'textarea';
  type?: string;
}

type InputProps = BaseInputProps &
  (InputHTMLAttributes<HTMLInputElement> | TextareaHTMLAttributes<HTMLTextAreaElement>);

const Input: React.FC<InputProps> = (props) => {
  const {
    label,
    error,
    helperText,
    className = '',
    showPasswordToggle = false,
    as = 'input',
    type,
    ...otherProps
  } = props;

  const [showPassword, setShowPassword] = useState(false);

  const isPasswordWithToggle = type === 'password' && showPasswordToggle && as === 'input';
  const inputType = isPasswordWithToggle ? (showPassword ? 'text' : 'password') : type;

  const baseClasses = `flex w-full rounded-md border ${
    error ? 'border-red-500' : 'border-input'
  } bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 ${className}`;

  const inputClasses = as === 'textarea'
    ? `${baseClasses} h-auto min-h-[80px]`
    : `${baseClasses} h-10`;

  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium mb-2 text-gray-700">
          {label}
        </label>
      )}
      <div className="relative">
        {as === 'textarea' ? (
          <textarea
            className={inputClasses}
            {...(otherProps as TextareaHTMLAttributes<HTMLTextAreaElement>)}
          />
        ) : (
          <input
            type={inputType}
            className={inputClasses}
            {...(otherProps as InputHTMLAttributes<HTMLInputElement>)}
          />
        )}
        {isPasswordWithToggle && (
          <button
            type="button"
            className="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-500 hover:text-gray-700"
            onClick={() => setShowPassword(!showPassword)}
          >
            {showPassword ? '🙈' : '👁️'} {/* Eye icon alternatives */}
          </button>
        )}
      </div>
      {error && (
        <p className="mt-1 text-sm text-red-600">{error}</p>
      )}
      {helperText && !error && (
        <p className="mt-1 text-sm text-gray-500">{helperText}</p>
      )}
    </div>
  );
};

export default Input;