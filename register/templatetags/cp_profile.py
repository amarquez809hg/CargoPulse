from django import template

from register.profile_cards import (
    broker_profile_card,
    carrier_profile_card,
    demo_broker_profile,
    demo_carrier_profile,
)

register = template.Library()


@register.inclusion_tag("register/includes/profile_card_carrier.html")
def render_carrier_profile_card(company=None, compact=False, mini=False):
    ctx = carrier_profile_card(company) if company else demo_carrier_profile()
    ctx["compact"] = compact
    ctx["mini"] = mini
    return ctx


@register.inclusion_tag("register/includes/profile_card_broker.html")
def render_broker_profile_card(profile=None, compact=False, mini=False):
    ctx = broker_profile_card(profile) if profile else demo_broker_profile()
    ctx["compact"] = compact
    ctx["mini"] = mini
    return ctx


@register.inclusion_tag("register/includes/profile_card_post.html")
def render_equipment_post_card(post, show_contact=False, list_row=False):
    return {"post": post, "show_contact": show_contact, "list_row": list_row}


@register.inclusion_tag("register/includes/profile_card_load.html")
def render_load_card(load, show_contact=False, list_row=False):
    return {"load": load, "show_contact": show_contact, "list_row": list_row}
