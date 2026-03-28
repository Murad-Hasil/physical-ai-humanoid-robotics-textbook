"""
Grok API client for LLM interactions.

Provides interface to xAI Grok API with hardware-aware prompt support.
"""

import logging
import time
import httpx
from typing import Optional, Dict, Any

from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class GrokClient:
    """
    Client for xAI Grok API.
    
    Handles API communication and response parsing.
    """
    
    def __init__(self):
        """Initialize Grok/Groq client. Auto-detects API provider from key prefix."""
        self.api_key = settings.grok_api_key
        self.model = settings.grok_model
        self.api_timeout = settings.grok_api_timeout
        self.max_retries = settings.grok_max_retries

        # Auto-detect provider: gsk_ = Groq, xai- = xAI Grok
        if self.api_key and self.api_key.startswith("gsk_"):
            self.base_url = "https://api.groq.com/openai/v1"
            # Map grok-beta -> groq-compatible model
            if self.model in ("grok-beta", "grok-2", "grok-3"):
                self.model = "llama-3.3-70b-versatile"
            logger.info(f"Using Groq API with model: {self.model}")
        else:
            self.base_url = "https://api.x.ai/v1"
            logger.info(f"Using xAI Grok API with model: {self.model}")
    
    async def generate(
        self,
        system_prompt: str,
        user_query: str,
        max_tokens: Optional[int] = 1024,
        temperature: Optional[float] = 0.7,
    ) -> str:
        """
        Generate response using Grok API.

        Args:
            system_prompt: System instructions (may include hardware context)
            user_query: User's query
            max_tokens: Maximum tokens in response
            temperature: Response creativity (0.0-1.0)

        Returns:
            str: Generated response text
        """
        logger.info(f"Calling Grok API with model: {self.model}")

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query},
        ]

        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        # Retry logic
        for attempt in range(self.max_retries):
            try:
                start_time = time.time()
                async with httpx.AsyncClient(timeout=self.api_timeout) as client:
                    response = await client.post(
                        f"{self.base_url}/chat/completions",
                        headers=headers,
                        json=payload,
                    )
                    llm_latency_ms = (time.time() - start_time) * 1000
                    logger.debug(f"Gro kAPI call completed in {llm_latency_ms:.2f}ms")

                    response.raise_for_status()

                    result = response.json()
                    assistant_message = result["choices"][0]["message"]["content"]

                    logger.info("Grok API call successful")
                    return assistant_message

            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error: {e.response.status_code}")
                if attempt == self.max_retries - 1:
                    raise
                await self._delay_retry(attempt)

            except httpx.TimeoutException as e:
                logger.error(f"Timeout error: {e}")
                if attempt == self.max_retries - 1:
                    raise GrokAPIError("Request timed out")
                await self._delay_retry(attempt)

            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                if attempt == self.max_retries - 1:
                    raise GrokAPIError(f"API call failed: {str(e)}")
                await self._delay_retry(attempt)

        raise GrokAPIError("Max retries exceeded")

    async def generate_personalized_summary(
        self,
        system_prompt: str,
        chapter_content: str,
        hardware_type: str,
        skill_level: str,
        hardware_details: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Generate personalized chapter summary.

        Args:
            system_prompt: Personalization prompt template
            chapter_content: Original chapter summary
            hardware_type: User's hardware (sim_rig, edge_kit, unitree)
            skill_level: User's skill level (beginner, intermediate, advanced)
            hardware_details: Additional hardware specs

        Returns:
            Dict with summary_content, tokens_used, generation_time_ms
        """
        from llm.prompts.personalization import format_hardware_details

        # Format hardware details
        hw_details_str = format_hardware_details(
            hardware_type,
            **(hardware_details or {})
        )

        # Build user query
        user_query = system_prompt.format(
            hardware_type=hardware_type,
            hardware_details=hw_details_str,
            skill_level=skill_level,
            original_summary=chapter_content,
        )

        # Generate response
        start_time = time.time()
        response = await self.generate(
            system_prompt="You are an expert technical educator.",
            user_query=user_query,
            max_tokens=2048,
            temperature=0.5,  # Lower temperature for consistency
        )
        generation_time_ms = (time.time() - start_time) * 1000

        # Estimate tokens (rough approximation)
        tokens_used = len(response.split()) * 1.3

        return {
            "summary_content": response,
            "tokens_used": int(tokens_used),
            "generation_time_ms": generation_time_ms,
        }

    async def generate_translation(
        self,
        system_prompt: str,
        content: str,
        language_code: str = "ur-Latn",
    ) -> Dict[str, Any]:
        """
        Generate translation to Roman Urdu.

        Args:
            system_prompt: Translation prompt template
            content: Content to translate
            language_code: Target language (default: ur-Latn)

        Returns:
            Dict with translated_content, tokens_used, generation_time_ms
        """
        # Build user query
        user_query = system_prompt.format(content=content)

        # Generate response
        start_time = time.time()
        response = await self.generate(
            system_prompt="You are an expert technical translator.",
            user_query=user_query,
            max_tokens=4096,
            temperature=0.3,  # Lower temperature for accuracy
        )
        generation_time_ms = (time.time() - start_time) * 1000

        # Estimate tokens
        tokens_used = len(response.split()) * 1.3

        return {
            "translated_content": response,
            "tokens_used": int(tokens_used),
            "generation_time_ms": generation_time_ms,
        }

    async def _delay_retry(self, attempt: int):
        """
        Delay before retry with exponential backoff.
        
        Args:
            attempt: Current attempt number
        """
        import asyncio
        delay = 2 ** attempt  # Exponential backoff
        await asyncio.sleep(delay)


class GrokAPIError(Exception):
    """Custom exception for Grok API errors."""
    pass
