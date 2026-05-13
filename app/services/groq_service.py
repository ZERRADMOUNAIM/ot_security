"""
Groq API Service for OTMindset.
Handles LLM calls, response parsing, and error handling.
"""

import os
import json
import logging
import re
from groq import Groq

from app.services.prompt_engine import build_system_prompt, build_analysis_prompt

logger = logging.getLogger(__name__)


class GroqService:
    """Service wrapper for Groq API interactions."""

    def __init__(self):
        self.api_key = os.environ.get('GROQ_API_KEY', '')
        self.model = os.environ.get('GROQ_MODEL', 'llama-3.3-70b-versatile')
        self.client = None
        if self.api_key:
            self.client = Groq(api_key=self.api_key)

    def _sanitize_input(self, user_input):
        """
        Sanitize user input to prevent prompt injection attacks.
        Strips control characters and known injection patterns.
        """
        # Remove potential injection patterns
        injection_patterns = [
            r'ignore\s+(all\s+)?previous\s+instructions',
            r'disregard\s+(all\s+)?above',
            r'forget\s+(all\s+)?previous',
            r'system\s*:\s*',
            r'assistant\s*:\s*',
            r'<\|.*?\|>',
            r'\[INST\]',
            r'\[/INST\]',
        ]

        sanitized = user_input.strip()
        for pattern in injection_patterns:
            sanitized = re.sub(pattern, '[FILTERED]', sanitized, flags=re.IGNORECASE)

        return sanitized

    def _parse_response(self, raw_content):
        """
        Parse the LLM response into a structured dict.
        Handles cases where the model wraps JSON in markdown code blocks.
        """
        content = raw_content.strip()

        # Remove markdown code block wrappers if present
        if content.startswith('```'):
            lines = content.split('\n')
            # Remove first line (```json or ```)
            lines = lines[1:]
            # Remove last line (```)
            if lines and lines[-1].strip() == '```':
                lines = lines[:-1]
            content = '\n'.join(lines)

        try:
            result = json.loads(content)
            return self._validate_structure(result)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM JSON response: {e}")
            logger.debug(f"Raw content: {content[:500]}")
            # Attempt to extract JSON from the response
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                try:
                    result = json.loads(json_match.group())
                    return self._validate_structure(result)
                except json.JSONDecodeError:
                    pass
            return self._get_fallback_response("Failed to parse AI response.")

    def _validate_structure(self, result):
        """Ensure the response has all required fields."""
        required_fields = [
            'what_you_should_know',
            'what_you_should_ask',
            'expected_risks',
            'recommended_controls'
        ]

        for field in required_fields:
            if field not in result:
                result[field] = []

        if 'references_and_standards' not in result or not isinstance(result['references_and_standards'], dict):
            result['references_and_standards'] = {
                'otcc': [],
                'iec_62443': [],
                'nist_sp_800_82': []
            }
        else:
            refs = result['references_and_standards']
            refs.setdefault('otcc', [])
            refs.setdefault('iec_62443', [])
            refs.setdefault('nist_sp_800_82', [])

        return result

    def _get_fallback_response(self, error_msg):
        """Return a structured fallback response on failure."""
        return {
            'what_you_should_know': [f'Analysis could not be completed: {error_msg}'],
            'what_you_should_ask': ['Unable to determine — please retry the analysis.'],
            'expected_risks': ['Analysis failure may indicate connectivity or configuration issues.'],
            'recommended_controls': ['Please retry the analysis or contact the administrator.'],
            'references_and_standards': {
                'otcc': [],
                'iec_62443': [],
                'nist_sp_800_82': []
            }
        }

    def analyze_ot_request(self, user_input):
        """
        Analyze an OT operational/cybersecurity request using the Groq LLM.
        
        Args:
            user_input: The user's OT scenario description.
            
        Returns:
            dict: Structured cybersecurity assessment.
        """
        if not self.client:
            logger.error("Groq client not initialized. Check GROQ_API_KEY.")
            return self._get_fallback_response("Groq API key not configured.")

        # Sanitize the input
        sanitized_input = self._sanitize_input(user_input)

        try:
            logger.info(f"Sending analysis request to Groq ({self.model})")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": build_system_prompt()
                    },
                    {
                        "role": "user",
                        "content": build_analysis_prompt(sanitized_input)
                    }
                ],
                temperature=0.3,
                max_tokens=4096,
                top_p=0.9,
            )

            raw_content = response.choices[0].message.content
            logger.info("Received response from Groq, parsing...")

            return self._parse_response(raw_content)

        except Exception as e:
            logger.error(f"Groq API error: {str(e)}")
            return self._get_fallback_response(f"AI engine error: {str(e)}")
