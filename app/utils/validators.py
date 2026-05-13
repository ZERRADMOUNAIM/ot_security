"""
Input validators and sanitization utilities.
"""

import re


# Maximum scenario length
MAX_SCENARIO_LENGTH = 2000
MIN_SCENARIO_LENGTH = 10

# Suspicious patterns for prompt injection
INJECTION_PATTERNS = [
    r'ignore\s+(all\s+)?previous\s+instructions',
    r'disregard\s+(all\s+)?above',
    r'forget\s+(all\s+)?previous',
    r'you\s+are\s+now',
    r'pretend\s+to\s+be',
    r'act\s+as\s+if',
    r'new\s+instruction',
    r'override\s+system',
    r'<script',
    r'javascript:',
    r'on\w+\s*=',
]


def validate_scenario(scenario):
    """
    Validate an OT scenario input.
    
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    if not scenario or not scenario.strip():
        return False, "Scenario cannot be empty."

    scenario = scenario.strip()

    if len(scenario) < MIN_SCENARIO_LENGTH:
        return False, f"Scenario must be at least {MIN_SCENARIO_LENGTH} characters."

    if len(scenario) > MAX_SCENARIO_LENGTH:
        return False, f"Scenario must not exceed {MAX_SCENARIO_LENGTH} characters."

    # Check for prompt injection attempts
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, scenario, re.IGNORECASE):
            return False, "Input contains potentially malicious content."

    return True, None


def sanitize_html(text):
    """Remove HTML tags from text."""
    return re.sub(r'<[^>]+>', '', str(text))


def validate_password(password):
    """
    Validate password strength.
    
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."

    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."

    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter."

    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one digit."

    return True, None


def validate_username(username):
    """
    Validate username format.
    
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    if not username or len(username) < 3:
        return False, "Username must be at least 3 characters."

    if len(username) > 30:
        return False, "Username must not exceed 30 characters."

    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores."

    return True, None


def validate_email(email):
    """
    Basic email format validation.
    
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email format."
    return True, None
