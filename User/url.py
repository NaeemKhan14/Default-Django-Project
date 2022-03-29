from django.urls import path
from django.contrib.auth import views
from User.forms import UserLoginForm, UserPasswordResetForm, ChangePasswordForm

urlpatterns = [
    path('login', views.LoginView.as_view(template_name='User/login.html',
                                          authentication_form=UserLoginForm,
                                          redirect_authenticated_user=True), name='login'),
    path('logout/', views.LogoutView.as_view(next_page='login'), name='logout'),
    path('password_reset/', views.PasswordResetView.as_view(template_name='User/password_reset_form.html',
                                                            form_class=UserPasswordResetForm), name='password_reset'),
    path('password_reset/done/',
         views.PasswordResetDoneView.as_view(template_name='User/password_reset_done.html'), name='password_reset_done'
         ),
    path('change_password/<uidb64>/<token>/',
         views.PasswordResetConfirmView.as_view(template_name='User/password_reset_confirm.html',
                                                form_class=ChangePasswordForm), name='password_reset_confirm'),
    path('password_reset_complete/',
         views.PasswordResetCompleteView.as_view(template_name='User/password_reset_complete.html'),
         name='password_reset_complete'),
]
