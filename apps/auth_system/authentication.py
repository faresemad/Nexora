from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError

from .conf import auth_settings


class CookieJWTAuthentication(JWTAuthentication):
    """
    Reads the JWT access token from an HttpOnly cookie instead of the
    Authorization header. Falls back gracefully (returns None) so views that
    allow unauthenticated access still work.
    """

    def authenticate(self, request):
        raw_token = request.COOKIES.get(auth_settings.JWT_ACCESS_COOKIE_NAME)
        if raw_token is None:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
        except TokenError:
            return None

        return self.get_user(validated_token), validated_token
