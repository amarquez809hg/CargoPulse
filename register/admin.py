from django.contrib import admin

from .models import TruckAvailability, TruckingCompany, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "display_name", "brokerage_name", "created_at")
    list_filter = ("role",)


@admin.register(TruckingCompany)
class TruckingCompanyAdmin(admin.ModelAdmin):
    list_display = ("company_name", "user", "email", "whatsapp", "hq_city", "created_at")
    search_fields = ("company_name", "email", "whatsapp", "hq_city")


@admin.register(TruckAvailability)
class TruckAvailabilityAdmin(admin.ModelAdmin):
    list_display = (
        "company",
        "lane_type",
        "port_of_entry",
        "current_city",
        "destination_city",
        "created_at",
    )
    list_filter = ("lane_type", "port_of_entry", "current_city", "destination_city")
    search_fields = (
        "company__company_name",
        "current_city",
        "destination_city",
    )
