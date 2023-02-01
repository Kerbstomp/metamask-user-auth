from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_routes, name='api-routes'),
    path('auth/', views.authenticate_user, name='authenticate-user'),
    path('users/', views.UsersView.as_view(), name='users'),
]
