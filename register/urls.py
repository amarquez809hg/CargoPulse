from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.auth_login, name="login"),
    path("logout/", views.auth_logout, name="logout"),
    path("signup/carrier/", views.carrier_signup, name="carrier_signup"),
    path("signup/broker/", views.broker_signup, name="broker_signup"),
    path("carrier/", views.carrier_dashboard, name="carrier_dashboard"),
    path("carrier/post/", views.carrier_post_truck, name="carrier_post"),
    path("broker/trucks/", views.broker_board, name="broker_board"),
]
