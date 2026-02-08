"""External Gemini client for connecting to the LLM via HTTP."""

import httpx
import json
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from ..core.config import config
from abc import ABC, abstractmethod


class LLMClientInterface(ABC):
    """Abstract interface for LLM clients."""

    @abstractmethod
    async def generate_response(self, prompt: str, tools: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Generate a response from the LLM."""
        pass


class GeminiClient(LLMClientInterface):
    """Client for interacting with Google Gemini via external HTTP client."""

    def __init__(self):
        self.api_key = config.GEMINI_API_KEY
        self.base_url = "https://generativelanguage.googleapis.com/v1"
        self.model = config.GEMINI_MODEL_NAME  # Use model from configuration

    async def generate_response(self, prompt: str, tools: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Generate a response from Gemini.

        Args:
            prompt: The input prompt for the LLM
            tools: Optional list of available tools for function calling

        Returns:
            Dict containing the LLM response
        """
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")

        # Prepare the request payload
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }

        # NOTE: Temporarily disabling tools due to API compatibility issues
        # Add tools if provided (only for models that support function calling)
        # if tools:
        #     payload["tools"] = [{"function_declarations": tools}]

        # Construct the API endpoint
        url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"

        # Make the API request
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                url,
                headers={
                    "Content-Type": "application/json"
                },
                json=payload
            )

            if response.status_code != 200:
                raise Exception(f"Gemini API request failed with status {response.status_code}: {response.text}")

            result = response.json()

            # Process the response
            if "candidates" in result and len(result["candidates"]) > 0:
                candidate = result["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    parts = candidate["content"]["parts"]
                    text_response = ""

                    for part in parts:
                        if "text" in part:
                            text_response += part["text"]

                    return {
                        "success": True,
                        "response": text_response,
                        "raw_response": result
                    }
                else:
                    return {
                        "success": False,
                        "error": "No content in response",
                        "raw_response": result
                    }
            else:
                return {
                    "success": False,
                    "error": "No candidates in response",
                    "raw_response": result
                }

    async def chat_completions(self, messages: List[Dict[str, str]], tools: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Generate a chat completion response from Gemini.

        Args:
            messages: List of messages in the conversation
            tools: Optional list of available tools for function calling

        Returns:
            Dict containing the LLM response
        """
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")

        # Convert messages to Gemini format
        contents = []
        for msg in messages:
            role = "model" if msg["role"] == "assistant" else "user"
            contents.append({
                "role": role,
                "parts": [
                    {
                        "text": msg["content"]
                    }
                ]
            })

        # Prepare the request payload
        payload = {
            "contents": contents
        }

        # NOTE: Temporarily disabling tools due to API compatibility issues
        # Add tools if provided (only for models that support function calling)
        # if tools:
        #     payload["tools"] = [{"function_declarations": tools}]

        # Construct the API endpoint
        url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"

        # Make the API request
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                url,
                headers={
                    "Content-Type": "application/json"
                },
                json=payload
            )

            if response.status_code != 200:
                raise Exception(f"Gemini API request failed with status {response.status_code}: {response.text}")

            result = response.json()

            # Process the response
            if "candidates" in result and len(result["candidates"]) > 0:
                candidate = result["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    parts = candidate["content"]["parts"]
                    text_response = ""

                    for part in parts:
                        if "text" in part:
                            text_response += part["text"]

                    return {
                        "success": True,
                        "response": text_response,
                        "raw_response": result
                    }
                else:
                    return {
                        "success": False,
                        "error": "No content in response",
                        "raw_response": result
                    }
            else:
                return {
                    "success": False,
                    "error": "No candidates in response",
                    "raw_response": result
                }


# Global instance of the Gemini client
gemini_client = GeminiClient()