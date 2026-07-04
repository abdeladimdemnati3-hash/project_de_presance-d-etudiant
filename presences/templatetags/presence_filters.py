from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Return dictionary[key] or None."""
    if dictionary:
        return dictionary.get(key)
    return None


@register.filter
def get_statut(presence):
    """Return the statut of a Presence object or empty string."""
    if presence:
        return presence.statut
    return ''
