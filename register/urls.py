from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("brokers/", views.info_brokers, name="info_brokers"),
    path("carriers/", views.info_carriers, name="info_carriers"),
    path("platform/equipment-board/", views.info_platform_equipment_board, name="info_platform_equipment_board"),
    path("platform/post-equipment/", views.info_platform_post_equipment, name="info_platform_post_equipment"),
    path("coverage/border-crossings/", views.info_coverage_border_crossings, name="info_coverage_border_crossings"),
    path("coverage/lanes/", views.info_coverage_lanes, name="info_coverage_lanes"),
    path("coverage/equipment/", views.info_coverage_equipment, name="info_coverage_equipment"),
    path("resources/how-it-works/", views.info_resources_how_it_works, name="info_resources_how_it_works"),
    path("resources/carrier-workflow/", views.info_resources_carrier_workflow, name="info_resources_carrier_workflow"),
    path("resources/broker-workflow/", views.info_resources_broker_workflow, name="info_resources_broker_workflow"),
    path("login/", views.auth_login, name="login"),
    path("logout/", views.auth_logout, name="logout"),
    path("signup/carrier/", views.carrier_signup, name="carrier_signup"),
    path("signup/broker/", views.broker_signup, name="broker_signup"),
    path("carrier/", views.carrier_dashboard, name="carrier_dashboard"),
    path("carrier/post/", views.carrier_post_truck, name="carrier_post"),
    path("broker/trucks/", views.broker_board, name="broker_board"),
]
