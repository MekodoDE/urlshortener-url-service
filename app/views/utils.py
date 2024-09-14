import random
import string
import uuid
from flask_smorest import abort
from flask_jwt_extended import get_jwt
from flask_jwt_extended.exceptions import JWTExtendedException


def generate_random_url_key(length=3):
    """
    Generate a random URL key consisting of letters and digits.
    
    Args:
        length (int): The length of the generated key. Defaults to 3.
        
    Returns:
        str: Randomly generated URL key.
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def get_jwt_claims():
    """
    Extract JWT claims and handle possible exceptions.
    
    Returns:
        tuple: A tuple containing the user's user_id (uuid) and role (str).
    """
    try:
        jwt_claims = get_jwt()
        user_id = uuid.UUID(jwt_claims.get("sub"))
        role = jwt_claims.get("role", "viewer")  # Default to 'viewer' if no role is present
        return user_id, role
    except JWTExtendedException:
        abort(401, message="Invalid or expired token")
    except ValueError:
        abort(400, message="Invalid user ID format")
