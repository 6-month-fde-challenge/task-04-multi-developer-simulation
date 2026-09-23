from config import api_key
from profile import profile_name


def power(a, b):
    """Return a raised to the power of b once the API key and profile are present."""
    if not api_key:
        print("No API key configured - cannot run exponentiation")
        return None
    if not profile_name:
        print("No logged-in profile - cannot run exponentiation")
        return None
    print("API key present and logged in as", profile_name)
    return a ** b
