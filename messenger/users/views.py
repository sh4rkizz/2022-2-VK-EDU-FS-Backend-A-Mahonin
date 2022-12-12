from django.shortcuts import get_list_or_404
from rest_framework.generics import RetrieveAPIView

from users.models import User
from users.serializers import UserSerializer


class UserView(RetrieveAPIView):
    """ Get user information """

    serializer_class = UserSerializer
    queryset = User.objects.all()
