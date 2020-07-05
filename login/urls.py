from django.urls import path
from . import views
urlpatterns = [
    path('login/',views.login),
    path('register/',views.register),
    path('logout/',views.logout),
    path('current/',views.getCurrentUser),
    path('change/',views.changePassword),
    path('reset/',views.resetPassword),
    path('confirm/',views.userConfirm),
    ]