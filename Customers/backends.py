from django.contrib.auth.backends import BaseBackend, ModelBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model


class CustomerBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None