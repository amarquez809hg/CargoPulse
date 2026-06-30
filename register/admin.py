from django.contrib import admin

from .models import BrokerLoad, TruckAvailability, TruckingCompany, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "display_name", "brokerage_name", "created_at")
    list_filter = ("role",)


@admin.register(TruckingCompany)
class TruckingCompanyAdmin(admin.ModelAdmin):
    list_display = (
        "company_name",
        "user",
        "email",
        "hq_city",
        "primary_port_of_entry",
        "ctpat_certified",
        "b1_drivers",
        "created_at",
    )
    list_filter = ("primary_port_of_entry", "hq_city", "ctpat_certified", "b1_drivers")
    search_fields = (
        "company_name",
        "email",
        "whatsapp",
        "hq_city",
        "company_address",
        "mexico_corridor",
        "us_corridor",
        "popular_destinations",
    )


@admin.register(TruckAvailability)
class TruckAvailabilityAdmin(admin.ModelAdmin):
    list_display = (
        "company",
        "lane_type",
        "port_of_entry",
        "location_address",
        "current_city",
        "destination_city",
        "ctpat_certified",
        "b1_drivers",
        "min_rate_per_mile",
        "created_at",
    )
    list_filter = (
        "post_status",
        "lane_type",
        "equipment_type",
        "port_of_entry",
        "load_type",
        "ctpat_certified",
        "b1_drivers",
    )
    search_fields = (
        "company__company_name",
        "current_city",
        "destination_city",
        "reference_id",
    )


@admin.register(BrokerLoad)
class BrokerLoadAdmin(admin.ModelAdmin):
    list_display = (
        "profile",
        "lane_type",
        "port_of_entry",
        "current_city",
        "ctpat_required",
        "b1_drivers_required",
        "created_at",
    )
    list_filter = (
        "post_status",
        "lane_type",
        "equipment_type",
        "port_of_entry",
        "load_type",
        "ctpat_required",
        "b1_drivers_required",
    )
    search_fields = (
        "profile__user__username",
        "profile__brokerage_name",
        "current_city",
        "reference_id",
        "mexico_corridor",
        "us_corridor",
    )
