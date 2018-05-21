from django.contrib.auth import authenticate as django_auth
from authentication.models import User

class MyCustomBackend(object):
    def authenticate(username=None, password=None):
        user = django_auth(username=username, password=password)
        if user and user.is_verified:
            return user
        else:
            return None