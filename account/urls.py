from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('', auth_views.LogoutView.as_view(next_page='account:login'), name='logout'),
]
