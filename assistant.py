"""
assistant.py
Core Customer Message Assistant powered by the official google-genai SDK.
Handles multi-turn chat memory, system instructions, and detailed API error reporting.
"""

import logging
import os
import time
from typing import Optional

from google import genai
from google.genai import errors, types

from knowledge_base import build_system_instruction

# Configure structured logging for debugging and production monitoring
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("CustomerAssistant")


class CustomerSupportAssistant:
    """Manages an interactive, stateful customer support chat session."""

    def __init__(
        self,
        model_name: str = "gemini-2.5-flash",
        api_key: Optional[str] = None,
        max_retries: int = 2,
    ) -> None:
        """
        Initializes the Gemini client and starts a new stateful chat session.

        Args:
            model_name: Gemini model identifier (default: gemini-2.5-flash).
            api_key: Optional explicit API key. Falls back to GEMINI_API_KEY env var.
            max_retries: Number of automatic retries on transient rate limits/server errors.
        """
        resolved_key = api_key or os.getenv("GEMINI_API_KEY")
        if not resolved_key:
            raise ValueError(
                "GEMINI_API_KEY is missing. Set it in your .env file or environment variables."
            )

        self.model_name = model_name
        self.max_retries = max_retries
        self.client = genai.Client(api_key=resolved_key)
        self.system_instruction = build_system_instruction()

        self._config = types.GenerateContentConfig(
            system_instruction=self.system_instruction,
            temperature=0.3,  # Low temperature keeps answers factual and policy-aligned
            max_output_tokens=1024,
        )

        self.chat_session = self._create_new_session()

    def _create_new_session(self):
        """Creates a fresh multi-turn chat session with the configured system prompt."""
        return self.client.chats.create(
            model=self.model_name,
            config=self._config,
        )

    def reset_conversation(self) -> None:
        """Clears conversation memory and starts a fresh customer session."""
        logger.info("Resetting customer chat session.")
        self.chat_session = self._create_new_session()

    def send_message(self, customer_message: str) -> str:
        """
        Sends a customer message to the chat session and returns the assistant's reply.
        Automatically preserves conversation history across turns.

        Args:
            customer_message: The raw message text from the customer.

        Returns:
            The assistant's formatted response text, or the exact API error message on failure.
        """
        cleaned_message = customer_message.strip()
        if not cleaned_message:
            return "Please enter a message so I can assist you."

        for attempt in range(self.max_retries + 1):
            try:
                response = self.chat_session.send_message(cleaned_message)

                if response and response.text:
                    return response.text.strip()

                logger.warning("Received empty response object from Gemini API.")
                return (
                    "I apologize, I couldn't generate a response right now. "
                    "Please try rephrasing your question or contact our support team."
                )

            except errors.APIError as api_err:
                logger.error(
                    "Gemini APIError (Code %s): %s", api_err.code, api_err.message
                )
                # Retry on transient rate limits (429) or temporary server issues (500, 503)
                if api_err.code in (429, 500, 503) and attempt < self.max_retries:
                    wait_seconds = 2 ** attempt
                    logger.info("Retrying in %s seconds...", wait_seconds)
                    time.sleep(wait_seconds)
                    continue

                return f"[Gemini API Error {api_err.code}]: {api_err.message}"

            except Exception as unexpected_err:
                logger.exception("Unexpected error during chat inference: %s", unexpected_err)
                return f"[Unexpected Error]: {type(unexpected_err).__name__} - {unexpected_err}"

        return "Unable to reach the assistant after multiple attempts."

