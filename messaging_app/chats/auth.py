"""Authentication helpers for chats app.

Expose commonly used DRF authentication classes so other modules can import them
from a single place (useful for tests/checks that expect this file to exist).
"""
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import BasicAuthentication, SessionAuthentication

# Default authentications to use in views
DEFAULT_AUTHENTICATIONS = [
    JWTAuthentication,
    BasicAuthentication,
    SessionAuthentication,
]

__all__ = [
    'JWTAuthentication',
    'BasicAuthentication',
    'SessionAuthentication',
    'DEFAULT_AUTHENTICATIONS',
]
