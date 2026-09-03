from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from apps.audit.services import AuditService

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    AuditService.log_action(
        action_type='LOGIN',
        module_name='accounts',
        description=f'User {user.email} successfully logged into WorkSphere.',
        object_id=str(user.id),
        object_repr=user.email,
        user=user,
        request=request
    )

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    if user:
        AuditService.log_action(
            action_type='LOGOUT',
            module_name='accounts',
            description=f'User {user.email} logged out.',
            object_id=str(user.id),
            object_repr=user.email,
            user=user,
            request=request
        )
