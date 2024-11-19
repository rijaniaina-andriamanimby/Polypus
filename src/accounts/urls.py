from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', login_user, name='login'),
    path('deconnexion/', logout_user, name='logout'),
    path('register/', register_user, name='register'),
    path('password_change/', password_change, name='ChangePassword'),
    path('admin_user/', list_user, name='listUser'),
    path('delete_user/<str:username>', delete_user, name='deleteUser'),
    path('update_user/<str:username>', user_update, name='update_user'),
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name='accounts/reset_password.html'),
         name='reset_password'),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/reset-password-done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.
         as_view(template_name='accounts/reset-password-confirm.html'),
         name='password_reset_confirm'),
    path('reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/reset-password-complete.html'),
         name='password_reset_complete')
]
