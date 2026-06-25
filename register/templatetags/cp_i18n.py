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
