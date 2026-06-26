from django.contrib import admin

from .models import TruckAvailability, TruckingCompany, UserProfile


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
        "created_at",
    )
    list_filter = ("primary_port_of_entry", "hq_city")
    search_fields = (
        "company_name",
        "email",
        "whatsapp",
        "hq_city",
        "company_address",
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
        "min_rate_per_mile",
        "created_at",
    )
    list_filter = (
        "post_status",
        "lane_type",
        "equipment_type",
        "port_of_entry",
        "load_type",
    )
    search_fields = (
        "company__company_name",
        "current_city",
        "destination_city",
        "reference_id",
    )
