from datetime import timedelta

from django.utils import timezone

POST_VISIBILITY_DAYS = 30


def visible_posts(queryset):
    """Posts listed for carriers and brokers (auto-expire after posted date)."""
    cutoff = timezone.now() - timedelta(days=POST_VISIBILITY_DAYS)
    return queryset.filter(created_at__gte=cutoff)


def visible_loads(queryset):
    """Broker load posts visible to carriers (same expiry window as equipment)."""
    return visible_posts(queryset)
