from utils import DynamicSerializer
from .models import User


# TODO add avatar
class UserSerializer(DynamicSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'is_online', 'last_seen_at', 'birthday', 'bio')
