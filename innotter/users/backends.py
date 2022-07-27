import jwt

from rest_framework import authentication, exceptions

from innotter.settings import JWT_SECRET
from users.models import User


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = "Bearer"

    def authenticate(self, request):
        request.user = None
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header or len(auth_header) != 2:
            return

        prefix = auth_header[0].decode("utf-8").lower()
        token = auth_header[1].decode("utf-8")

        if prefix != auth_header_prefix:
            return

        user, token = self.authenticate_credentials(request, token)
        
        return user, token

    def authenticate_credentials(self, request, token):
        try:
            payload = jwt.decode(jwt=token, key=JWT_SECRET, algorithms=["HS256"])
        except Exception as e:
            raise exceptions.AuthenticationFailed("Unable to decode token!")

        try:
            user = User.objects.get(pk=payload["user_id"])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("User doesn't found!")

        if not user.is_active:
            raise exceptions.AuthenticationFailed("User doen't active!")

        return user, token
    