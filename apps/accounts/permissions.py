from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def role_required(*role_codes):
    """
    Decorator checking role authorization with graceful fallback.
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
            messages.warning(request, f"You need {' or '.join(role_codes)} role to access this module.")
            return redirect('core:dashboard')
        return _wrapped_view
    return decorator

def permission_required(module, action='view'):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            if request.user.is_superuser or getattr(request.user, 'is_super_admin', False):
                return view_func(request, *args, **kwargs)
            if request.user.has_module_perm(module, action):
                return view_func(request, *args, **kwargs)
            messages.warning(request, f"Access restricted for action '{module}:{action}'.")
            return redirect('core:dashboard')
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
        messages.warning(request, "Permission required for this action.")
        return redirect('core:dashboard')
