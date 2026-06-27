from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class PortOfEntry(models.TextChoices):
    LAREDO = "LAREDO", "Laredo"
    EL_PASO = "EL_PASO", "El Paso"
    TIJUANA = "TIJUANA", "Tijuana"


class UserProfile(models.Model):
    ROLE_CARRIER = "carrier"
    ROLE_BROKER = "broker"
    ROLE_CHOICES = [
        (ROLE_CARRIER, _("Carrier")),
        (ROLE_BROKER, _("Broker")),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    display_name = models.CharField(max_length=120, blank=True)
    brokerage_name = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


class TruckingCompany(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="trucking_company",
        null=True,
        blank=True,
    )
    company_name = models.CharField(max_length=200)
    email = models.EmailField()
    whatsapp = models.CharField(max_length=30)
    company_address = models.CharField(max_length=255, blank=True)
    hq_city = models.CharField(max_length=120)
    hq_state = models.CharField(max_length=120, blank=True)
    primary_port_of_entry = models.CharField(
        max_length=20,
        choices=PortOfEntry.choices,
        blank=True,
        verbose_name=_("Primary border crossing"),
    )
    popular_destinations = models.TextField(
        blank=True,
        help_text=_("Corridors or cities you run often, e.g. Houston, Dallas, Laredo"),
    )
    ctpat_certified = models.BooleanField(default=False)
    b1_drivers = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.company_name


class TruckAvailability(models.Model):
    class LaneType(models.TextChoices):
        LANE = "LANE", _("Lane")
        POTENTIAL_LANE = "POTENTIAL_LANE", _("Potential Lane")
        SPOT_LANE = "SPOT_LANE", _("Spot Lane")

    class EquipmentType(models.TextChoices):
        VAN = "VAN", _("Van")
        REEFER = "REEFER", _("Reefer")
        FLATBED = "FLATBED", _("Flatbed")
        STEP_DECK = "STEP_DECK", _("Step deck")
        POWER_ONLY = "POWER_ONLY", _("Power only")
        OTHER = "OTHER", _("Other")

    class LoadType(models.TextChoices):
        FULL = "FULL", _("Full")
        PARTIAL = "PARTIAL", _("Partial")

    class PostStatus(models.TextChoices):
        OPEN = "OPEN", _("Open")
        BOOKED = "BOOKED", _("Booked")
        EXPIRED = "EXPIRED", _("Expired")

    company = models.ForeignKey(
        TruckingCompany, on_delete=models.CASCADE, related_name="posts"
    )
    lane_type = models.CharField(
        max_length=20,
        choices=LaneType.choices,
        default=LaneType.LANE,
    )
    port_of_entry = models.CharField(
        max_length=20, choices=PortOfEntry.choices, blank=True
    )
    location_address = models.CharField(max_length=255, blank=True)
    current_city = models.CharField(max_length=120)
    current_state = models.CharField(max_length=120, blank=True)
    destination_city = models.CharField(max_length=120, blank=True)
    destination_state = models.CharField(max_length=120, blank=True)
    equipment_type = models.CharField(
        max_length=20,
        choices=EquipmentType.choices,
        default=EquipmentType.VAN,
    )
    trailer_length_ft = models.PositiveSmallIntegerField(default=53)
    load_type = models.CharField(
        max_length=20,
        choices=LoadType.choices,
        default=LoadType.FULL,
    )
    weight_lbs = models.PositiveIntegerField(null=True, blank=True)
    min_rate_per_mile = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    reference_id = models.CharField(max_length=64, blank=True)
    post_status = models.CharField(
        max_length=20,
        choices=PostStatus.choices,
        default=PostStatus.OPEN,
    )
    equipment_notes = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "truck availabilities"

    def __str__(self):
        route = f"{self.current_city} → {self.destination_city or 'open'}"
        return f"{self.company.company_name} — {self.get_lane_type_display()}: {route}"
