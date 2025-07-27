import random
import string

def generate_random_alphanumeric_code(length):
    """
    Generates a random alphanumeric code of a specified length.

    Args:
        length (int): The desired length of the random code.

    Returns:
        str: A random string composed of uppercase letters, lowercase letters, and digits.
    """
    # Define the pool of characters: all ASCII letters (uppercase and lowercase) and digits
    characters = string.ascii_letters + string.digits

    # Use random.choices to pick 'length' characters from the pool
    # and then join them to form the final string
    random_code = ''.join(random.choices(characters, k=length))

    return random_code