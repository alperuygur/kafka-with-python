import random
import string


def generate_random_key(length=8):
    """Generate a random key of specified length."""
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))
