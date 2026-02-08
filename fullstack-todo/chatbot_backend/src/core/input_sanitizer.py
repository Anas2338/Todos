"""Input sanitization utilities for the AI Chatbot Backend."""

import html
import re
from typing import Union, List, Dict, Any


class InputSanitizer:
    """Utility class for sanitizing user inputs to prevent injection attacks."""

    @staticmethod
    def sanitize_string(input_str: str) -> str:
        """
        Sanitize a string input to prevent injection attacks.

        Args:
            input_str: The input string to sanitize

        Returns:
            Sanitized string safe for processing
        """
        if not input_str or not isinstance(input_str, str):
            return input_str

        # Escape HTML entities to prevent XSS
        sanitized = html.escape(input_str)

        # Remove potentially dangerous patterns
        # Remove script tags (case-insensitive)
        sanitized = re.sub(r'<script[^>]*>.*?</script>', '', sanitized, flags=re.IGNORECASE | re.DOTALL)

        # Remove javascript: and vbscript: protocols
        sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)
        sanitized = re.sub(r'vbscript:', '', sanitized, flags=re.IGNORECASE)

        # Remove data: and file: protocols (potential XSS vectors)
        sanitized = re.sub(r'data:', '', sanitized, flags=re.IGNORECASE)
        sanitized = re.sub(r'file:', '', sanitized, flags=re.IGNORECASE)

        # Remove potentially dangerous SQL injection patterns
        # This is a basic implementation - in production, use parameterized queries
        dangerous_sql_patterns = [
            r"(\b|\s)UNION(\b|\s)",  # UNION statements
            r"(\b|\s)DROP(\b|\s)",   # DROP statements
            r"(\b|\s)DELETE(\b|\s)", # DELETE statements
            r"(\b|\s)INSERT(\b|\s)", # INSERT statements
            r"(\b|\s)UPDATE(\b|\s)", # UPDATE statements
            r"(\b|\s)EXEC(\b|\s)",   # EXEC statements
            r"(\b|\s)SELECT(\b|\s)", # SELECT statements
            r"--",                    # SQL comment
            r";",                     # Statement terminator
            r"\'",                    # Quote
            r"\\",                    # Backslash
        ]

        for pattern in dangerous_sql_patterns:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)

        return sanitized.strip()

    @staticmethod
    def sanitize_dict(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitize a dictionary recursively.

        Args:
            data: The dictionary to sanitize

        Returns:
            Sanitized dictionary
        """
        if not isinstance(data, dict):
            return data

        sanitized_dict = {}
        for key, value in data.items():
            # Sanitize the key as well
            clean_key = InputSanitizer.sanitize_string(str(key)) if isinstance(key, str) else key

            if isinstance(value, str):
                sanitized_dict[clean_key] = InputSanitizer.sanitize_string(value)
            elif isinstance(value, dict):
                sanitized_dict[clean_key] = InputSanitizer.sanitize_dict(value)
            elif isinstance(value, list):
                sanitized_dict[clean_key] = InputSanitizer.sanitize_list(value)
            else:
                sanitized_dict[clean_key] = value

        return sanitized_dict

    @staticmethod
    def sanitize_list(data: List[Any]) -> List[Any]:
        """
        Sanitize a list recursively.

        Args:
            data: The list to sanitize

        Returns:
            Sanitized list
        """
        if not isinstance(data, list):
            return data

        sanitized_list = []
        for item in data:
            if isinstance(item, str):
                sanitized_list.append(InputSanitizer.sanitize_string(item))
            elif isinstance(item, dict):
                sanitized_list.append(InputSanitizer.sanitize_dict(item))
            elif isinstance(item, list):
                sanitized_list.append(InputSanitizer.sanitize_list(item))
            else:
                sanitized_list.append(item)

        return sanitized_list

    @staticmethod
    def validate_json_input(data: Union[str, Dict[str, Any]]) -> bool:
        """
        Validate that JSON input is safe and properly formatted.

        Args:
            data: The data to validate (either JSON string or parsed dict)

        Returns:
            True if input is safe and valid, False otherwise
        """
        import json

        if isinstance(data, str):
            try:
                parsed_data = json.loads(data)
            except json.JSONDecodeError:
                return False
        else:
            parsed_data = data

        # For safety, recursively check the data structure
        def is_safe_value(value):
            if isinstance(value, (str, int, float, bool, type(None))):
                return True
            elif isinstance(value, dict):
                return all(is_safe_value(v) for v in value.values())
            elif isinstance(value, list):
                return all(is_safe_value(item) for item in value)
            else:
                return False

        return is_safe_value(parsed_data)


# Global sanitizer instance
sanitizer = InputSanitizer()