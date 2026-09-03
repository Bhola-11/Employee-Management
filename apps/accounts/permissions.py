from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages

def role_required(*role_codes):
    """
    Decorator for views that checks if the user has any of the specified role codes.
    Superusers bypass role checks.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            if request.user.is_superuser or getattr(request.user, 'is_super_admin', False):
                return view_func(request, *args, **kwargs)
            if request.user.has_role(*role_codes):
                return view_func(request, *args, **kwargs)
            messages.error(request, 'Access Denied: You do not possess the required permissions for this action.')
            raise PermissionDenied
        return _wrapped_view
    return decorator

def permission_required(module, action='view'):
    """
    Decorator checking fine-grained module-action permissions.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            if request.user.is_superuser or getattr(request.user, 'is_super_admin', False):
                return view_func(request, *args, **kwargs)
            if request.user.has_module_perm(module, action):
                return view_func(request, *args, **kwargs)
            messages.error(request, f'Access Denied: You lack "{module}:{action}" permission.')
            raise PermissionDenied
        return _wrapped_view
    return decorator

class RoleRequiredMixin:
    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if request.user.is_superuser or getattr(request.user, 'is_super_admin', False):
            return super().dispatch(request, *args, **kwargs)
        if request.user.has_role(*self.allowed_roles):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied
