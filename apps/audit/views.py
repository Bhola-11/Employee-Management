from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ActivityLog
from apps.core.utils import paginate_queryset

@login_required
def audit_log_list_view(request):
    org = request.organization
    logs = ActivityLog.objects.filter(organization=org).select_related('user')
    
    action = request.GET.get('action')
    module = request.GET.get('module')
    
    if action:
        logs = logs.filter(action_type=action)
    if module:
        logs = logs.filter(module_name=module)

    page_obj = paginate_queryset(request, logs, 20)
    
    return render(request, 'audit/log_list.html', {
        'page_obj': page_obj,
        'logs': page_obj.object_list,
        'actions': ActivityLog.ACTION_CHOICES,
        'selected_action': action,
        'selected_module': module,
    })

@login_required
def audit_log_detail_view(request, pk):
    org = request.organization
    log_entry = get_object_or_404(
        ActivityLog.objects.prefetch_related('field_changes').select_related('user'),
        pk=pk,
        organization=org
    )
    return render(request, 'audit/log_detail.html', {'log': log_entry})
