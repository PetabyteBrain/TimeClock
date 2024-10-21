"""
Utility functions (e.g., for validation)

Functions:
 - is_valid_email(email): Validates an email address format.
"""
import re

def is_valid_email(email):
    """
    Validates an email address format.

    Parameters:
        email (str): The email address to validate.

    Returns:
        bool: True if the email address is valid, False otherwise.
    """
    # Improved regex pattern for email validation
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None
