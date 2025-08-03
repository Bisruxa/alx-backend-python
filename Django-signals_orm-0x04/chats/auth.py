# chats/auth.py (optional utility file for authentication)

from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

def login_user(email, password):
    user = authenticate(username=email, password=password)
    if user is None:
        raise AuthenticationFailed("Invalid credentials")
    return user
