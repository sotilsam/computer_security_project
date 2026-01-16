from django.urls import path
from Communication_LTD import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('forgot_password/', views.forgot_password_view, name='forgot_password'),
    path('verify/', views.verify_code_view, name='verify'),
    path('reset_password/', views.reset_password_view, name='reset_password'),
    path('change_password/', views.change_password_view, name='change_password'),
    path('logout/', views.logout_view, name='logout'),
]



