from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def currency(value, currency_symbol='$'):
    if value is None or value == '':
        return f'{currency_symbol}0.00'
    try:
        val = float(value)
        return f'{currency_symbol}{val:,.2f}'
    except (ValueError, TypeError):
        return f'{currency_symbol}{value}'

@register.filter
def status_badge(status):
    if not status:
        return ''
    status_str = str(status).upper()
    badge_map = {
        'ACTIVE': 'success',
        'CONFIRMED': 'success',
        'APPROVED': 'success',
        'HIRED': 'success',
        'COMPLETED': 'success',
        'PRESENT': 'success',
        'PAID': 'success',
        'RESOLVED': 'success',
        'VERIFIED': 'success',

        'PENDING': 'warning',
        'PROBATION': 'warning',
        'IN_REVIEW': 'warning',
        'SCREENING': 'warning',
        'SHORTLISTED': 'warning',
        'INTERVIEW': 'info',
        'ON_LEAVE': 'warning',
        'PROCESSING': 'info',
        'IN_PROGRESS': 'info',
        'OPEN': 'warning',
        'ASSIGNED': 'info',

        'REJECTED': 'danger',
        'TERMINATED': 'danger',
        'CANCELLED': 'danger',
        'EXITED': 'danger',
        'ABSENT': 'danger',
        'OVERDUE': 'danger',
        'UNPAID': 'danger',
        'SUSPENDED': 'danger',

        'NOTICE_PERIOD': 'secondary',
        'DRAFT': 'secondary',
        'ONBOARDING': 'info',
        'OFFER_SENT': 'info',
        'HOLIDAY': 'primary',
        'WEEKEND': 'light',
    }
    badge_class = badge_map.get(status_str, 'secondary')
    formatted = status_str.replace('_', ' ').title()
    html = f'<span class=badge badge-{badge_class}>{formatted}</span>'
    return mark_safe(html)

@register.filter
def get_item(dictionary, key):
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None

@register.filter
def mask(val, visible_end=4):
    if not val:
        return ''
    val = str(val)
    if len(val) <= int(visible_end):
        return val
    return '*' * (len(val) - int(visible_end)) + val[-int(visible_end):]

@register.simple_tag
def has_role(user, *roles):
    if not user.is_authenticated:
        return False
    if user.is_superuser or getattr(user, 'is_super_admin', False):
        return True
    user_roles = [r.role.code for r in user.role_assignments.all()]
    if getattr(user, 'active_role', None):
        user_roles.append(user.active_role.code)
    for r in roles:
        if r in user_roles:
            return True
    return False
