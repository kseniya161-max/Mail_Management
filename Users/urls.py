from django.urls import path
from Users.views import CreateUserView, confirm_email, CustomLoginView, CustomLogoutView, CustomPasswordResetView, CustomPasswordResetDoneView
from django.contrib.auth import views as auth_views
from Users.views import CustomPasswordResetCompleteView, CustomPasswordResetConfirmView, UserListView
from Users.views import BlockUserView, UnblockUserView, BlockUserConfirmationView, UnBlockUserConfirmationView, UserDetailView


app_name = "Users"

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
    path('confirm/<uidb64>/<token>/', confirm_email, name='confirm_email'),
    path('login/', CustomLoginView.as_view() , name='login'),
    path('logout/', CustomLogoutView.as_view() , name='logout'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('list/', UserListView.as_view(), name='user_list'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('user/<int:user_id>/block/', BlockUserView.as_view(), name='user_block'),
    path('user/<int:user_id>/unblock/', UnblockUserView.as_view(), name='user_unblock'),
    path('user/<int:user_id>/block/confirm/', BlockUserConfirmationView.as_view(), name='user_block_confirm'),
    path('user/<int:user_id>/unblock/confirm/', UnBlockUserConfirmationView.as_view(), name='user_unblock_confirm'),
]
