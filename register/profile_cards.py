from django.utils.translation import gettext as _

from .availability import visible_posts


def carrier_profile_card(company):
    """Build template context for a carrier profile card from a TruckingCompany."""
    posts = visible_posts(company.posts.all())
    equipment_counts = {}
    for post in posts:
        label = post.get_equipment_type_display()
        equipment_counts[label] = equipment_counts.get(label, 0) + 1

    equipment_parts = [
        f"{label} ({count})" for label, count in sorted(equipment_counts.items())
    ]
    contact_name = company.user.username if company.user_id else _("Fleet contact")

    return {
        "company": company,
        "contact_name": contact_name,
        "active_posts": posts.count(),
        "equipment_summary": ", ".join(equipment_parts) if equipment_parts else "—",
        "demo": False,
    }


def broker_profile_card(profile):
    """Build template context for a broker profile card from a UserProfile."""
    user = profile.user
    return {
        "profile": profile,
        "display_name": profile.display_name or user.username,
        "brokerage_name": profile.brokerage_name or _("Independent broker"),
        "email": user.email,
        "demo": False,
    }


def demo_carrier_profile():
    return {
        "company": None,
        "contact_name": "Marco Delgado",
        "company_name": "Transportes Del Norte",
        "company_initial": "TD",
        "role_label": _("Owner · dispatcher"),
        "location_line": "Monterrey, NL · Laredo crossing",
        "hq_city": "Monterrey, NL",
        "address": "Av. Industria 2400, Monterrey",
        "crossing": "Laredo",
        "destinations": "Houston, Dallas, San Antonio",
        "mexico_corridor": "Tijuana, Juarez, Nuevo Laredo",
        "us_corridor": "Houston, Dallas, San Antonio",
        "whatsapp": "+52 81 555 0142",
        "email": "contacto@delnorte.mx",
        "active_posts": 3,
        "equipment_summary": _("Van (2), Reefer (1)"),
        "ctpat_certified": True,
        "b1_drivers": True,
        "demo": True,
    }


def demo_broker_profile():
    return {
        "profile": None,
        "display_name": "Ana Ruiz",
        "brokerage_name": "Horizon Freight Partners",
        "broker_initial": "HF",
        "role_label": _("US freight broker"),
        "location_line": "Laredo, TX · US–Mexico lanes",
        "email": "ana@horizonfreight.com",
        "board_focus": _("Crossings, dry van, reefer"),
        "demo": True,
    }
