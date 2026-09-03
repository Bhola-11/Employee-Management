import random
import string
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def generate_random_code(prefix='WSP', length=6):
    digits = ''.join(random.choices(string.digits, k=length))
    return f'{prefix}-{digits}'

def generate_employee_id(org_code='WSP', next_num=1):
    return f'{org_code}-{next_num:05d}'

def mask_string(val, visible_end=4):
    if not val:
        return ''
    val = str(val)
    if len(val) <= visible_end:
        return val
    return '*' * (len(val) - visible_end) + val[-visible_end:]

def paginate_queryset(request, queryset, per_page=15):
    paginator = Paginator(queryset, per_page)
    page = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
    return ip
