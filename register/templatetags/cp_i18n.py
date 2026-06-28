from django import template
from django.utils.translation import gettext as _

register = template.Library()

LANE_TYPE_LABELS = {
    "LANE": lambda: _("Lane"),
    "POTENTIAL_LANE": lambda: _("Potential Lane"),
    "SPOT_LANE": lambda: _("Spot Lane"),
}


@register.filter
def lane_type_label(value):
    if not value:
        return "—"
    factory = LANE_TYPE_LABELS.get(value)
    return str(factory()) if factory else value


@register.filter
def cp_initials(value):
    if not value:
        return "?"
    parts = str(value).split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[1][0]).upper()
    return str(value)[:2].upper()
