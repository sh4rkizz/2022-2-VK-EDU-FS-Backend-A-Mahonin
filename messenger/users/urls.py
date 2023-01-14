from django.urls import path

from .views import UserView, CurrentUserView

urlpatterns = [
    path('info/<int:pk>', UserView.as_view(), name='user-info'),
    path('current/', CurrentUserView.as_view(), name='get-current-user')

    # path('', user_list, name='user list'),
    # path('<int:pku>', user_info, name='user info'),
    # path('edit/<int:pku>', edit_user, name='edit user profile')
]
