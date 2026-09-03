from .models import ActivityLog, ModelChangeLog
from apps.core.middleware import get_current_request, get_current_user, get_current_organization
from apps.core.utils import get_client_ip

class AuditService:
    @staticmethod
    def log_action(action_type, module_name, description, object_id='', object_repr='', changes=None, user=None, org=None, request=None):
        if not request:
            request = get_current_request()
        
        if not user:
            user = get_current_user() if request else None
            
        if not org:
            org = get_current_organization() if request else (getattr(user, 'organization', None) if user else None)

        ip = get_client_ip(request) if request else '127.0.0.1'
        ua = request.META.get('HTTP_USER_AGENT', 'System/Internal') if request else 'System/Internal'

        log_entry = ActivityLog.objects.create(
            organization=org,
            user=user,
            action_type=action_type,
            module_name=module_name,
            object_id=str(object_id),
            object_repr=str(object_repr)[:250],
            description=description,
            ip_address=ip,
            user_agent=ua,
            changes_json=changes or {}
        )

        if changes and isinstance(changes, dict):
            for field, vals in changes.items():
                if isinstance(vals, (list, tuple)) and len(vals) == 2:
                    old_v, new_v = vals
                else:
                    old_v, new_v = '', str(vals)
                ModelChangeLog.objects.create(
                    activity=log_entry,
                    field_name=field,
                    old_value=str(old_v),
                    new_value=str(new_v)
                )
        return log_entry

    @classmethod
    def log_activity(cls, organization=None, user=None, module='', action='UPDATE', obj=None, description=''):
        obj_id = getattr(obj, 'id', '') if obj else ''
        obj_repr = str(obj) if obj else ''
        return cls.log_action(
            action_type=action,
            module_name=module,
            description=description,
            object_id=obj_id,
            object_repr=obj_repr,
            user=user,
            org=organization
        )
