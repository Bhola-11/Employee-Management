import threading
from django.utils.deprecation import MiddlewareMixin
from apps.organizations.models import Organization

_thread_locals = threading.local()

def get_current_request():
    return getattr(_thread_locals, 'request', None)

def get_current_user():
    request = get_current_request()
    if request and hasattr(request, 'user'):
        return request.user
    return None

def get_current_organization():
    return getattr(_thread_locals, 'organization', None)

class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        _thread_locals.request = request
        org = None
        if request.user.is_authenticated:
            org_id = request.session.get('active_organization_id')
            if org_id:
                try:
                    org = Organization.objects.get(id=org_id, is_active=True)
                except Organization.DoesNotExist:
                    org = getattr(request.user, 'organization', None)
            else:
                org = getattr(request.user, 'organization', None)
                
        # If user has no explicit org assigned, fallback to primary active org
        if not org:
            org = Organization.objects.filter(is_active=True).first()
            
        request.organization = org
        request.tenant_org = org
        _thread_locals.organization = org

    def process_response(self, request, response):
        if hasattr(_thread_locals, 'request'):
            del _thread_locals.request
        if hasattr(_thread_locals, 'organization'):
            del _thread_locals.organization
        return response

class AuditMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.audit_ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
        request.audit_user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
