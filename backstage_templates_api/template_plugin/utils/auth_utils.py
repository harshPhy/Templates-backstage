"""
Authentication Utilities

This module provides utility functions for handling authentication.
"""

import logging
import uuid
import time
import jwt
from typing import Dict, Any, Optional

logger = logging.getLogger("auth-utils")

# JWT signing key - in production, this should be a secure key loaded from environment or secrets management
JWT_SECRET = "template-plugin-secret-key"  # For demo purposes only
JWT_ALGORITHM = "HS256"
JWT_EXPIRY = 3600  # 1 hour


def generate_token(subject: str, claims: Optional[Dict[str, Any]] = None) -> str:
    """
    Generate a JWT token.
    
    Args:
        subject: Subject of the token (typically user ID)
        claims: Additional claims to include in the token
        
    Returns:
        JWT token
    """
    try:
        logger.debug(f"Generating token for subject: {subject}")
        
        # Set up token payload
        now = int(time.time())
        payload = {
            "sub": subject,
            "iat": now,
            "exp": now + JWT_EXPIRY,
            "jti": str(uuid.uuid4())
        }
        
        # Add custom claims
        if claims:
            payload.update(claims)
            
        # Generate token
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        
        return token
    except Exception as e:
        logger.error(f"Error generating token: {str(e)}")
        raise ValueError(f"Failed to generate token: {str(e)}")


def validate_token(token: str) -> Dict[str, Any]:
    """
    Validate a JWT token.
    
    Args:
        token: JWT token to validate
        
    Returns:
        Token payload if valid
        
    Raises:
        ValueError: If the token is invalid
    """
    try:
        logger.debug("Validating token")
        
        # Decode and validate token
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("Token has expired")
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError as e:
        logger.warning(f"Invalid token: {str(e)}")
        raise ValueError(f"Invalid token: {str(e)}")
    except Exception as e:
        logger.error(f"Error validating token: {str(e)}")
        raise ValueError(f"Failed to validate token: {str(e)}")


def get_auth_headers(token: Optional[str] = None, subject: Optional[str] = None) -> Dict[str, str]:
    """
    Get authorization headers for HTTP requests.
    
    Either provide a token, or a subject to generate a new token.
    
    Args:
        token: Existing JWT token
        subject: Subject to generate a token for
        
    Returns:
        Authorization headers
        
    Raises:
        ValueError: If neither token nor subject is provided
    """
    if not token and not subject:
        raise ValueError("Either token or subject must be provided")
        
    if not token:
        token = generate_token(subject)
    return {"Authorization": f"Bearer {token}"}
