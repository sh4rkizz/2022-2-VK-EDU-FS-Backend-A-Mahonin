from utils import DynamicSerializer
from .models import User


class UserSerializer(DynamicSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'isOnline', 'lastSeenAt', 'birthday', 'bio')
