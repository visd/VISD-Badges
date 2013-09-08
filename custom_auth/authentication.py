from rest_framework.authentication import BaseAuthentication, TokenAuthentication
from django.contrib.auth import get_user_model


User = get_user_model()

class Authentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        username = request.META.get('X_USERNAME')
        if not username:
            return None

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, None)