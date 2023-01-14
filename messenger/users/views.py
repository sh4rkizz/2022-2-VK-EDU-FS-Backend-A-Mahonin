from rest_framework.generics import RetrieveAPIView

from users.models import User
from users.serializers import UserSerializer


class UserView(RetrieveAPIView):
    """ Get user information """

    serializer_class = UserSerializer
    queryset = User.objects.all()


class CurrentUserView(RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return User.objects.filter(id=self.request.user.id).first()
