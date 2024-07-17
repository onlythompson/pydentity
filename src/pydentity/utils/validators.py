import re
from pydantic import EmailStr, ValidationError

from pydentity.core.config import get_settings


settings = get_settings()

def validate_password(password: str) -> bool:
    """
    Validate the password against the defined rules.
    
    Rules:
    1. Minimum length as defined in settings
    2. At least one uppercase letter
    3. At least one lowercase letter
    4. At least one digit
    5. At least one special character
    
    :param password: The password to validate
    :return: True if valid, False otherwise
    """
    if len(password) < settings.MIN_PASSWORD_LENGTH:
        return False
    
    # Check for at least one uppercase letter
    if not re.search(r"[A-Z]", password):
        return False
    
    # Check for at least one lowercase letter
    if not re.search(r"[a-z]", password):
        return False
    
    # Check for at least one digit
    if not re.search(r"\d", password):
        return False
    
    # Check for at least one special character
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    
    return True

def validate_email(email: str) -> bool:
    """
    Validate the email using Pydantic's EmailStr.
    
    :param email: The email to validate
    :return: True if valid, False otherwise
    """
    try:
        EmailStr.validate(email)
        return True
    except ValidationError:
        return False

def validate_username(username: str) -> bool:
    """
    Validate the username against defined rules.
    
    Rules:
    1. 3-30 characters long
    2. Can contain letters, numbers, underscores, and hyphens
    3. Must start with a letter
    
    :param username: The username to validate
    :return: True if valid, False otherwise
    """
    username_pattern = r"^[a-zA-Z][a-zA-Z0-9_-]{2,29}$"
    return bool(re.match(username_pattern, username))

def validate_api_key(api_key: str) -> bool:
    """
    Validate the API key format.
    
    Rules:
    1. 32 characters long
    2. Contains only hexadecimal characters
    
    :param api_key: The API key to validate
    :return: True if valid, False otherwise
    """
    api_key_pattern = r"^[a-fA-F0-9]{32}$"
    return bool(re.match(api_key_pattern, api_key))