from django import template

register = template.Library()


@register.filter(name="split")
def split_filter(value, sep=","):
    try:
        return value.split(sep)
    except Exception:
        return []


@register.filter(name="strip")
def strip_filter(value):
    try:
        return value.strip()
    except Exception:
        return value


@register.filter(name="splitcsv")
def splitcsv_filter(value):
    """Split comma-separated values and return trimmed list"""
    try:
        return [item.strip() for item in value.split(",") if item.strip()]
    except Exception:
        return []


@register.filter(name="peso")
def peso_filter(value):
    """Format number as PHP currency"""
    try:
        return f"₱{int(value or 0):,}"
    except (ValueError, TypeError):
        return "₱0"


