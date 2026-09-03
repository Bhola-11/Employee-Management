import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.accounts.permissions import role_required
from .services import AnalyticsService
from .models import ScheduledReport

@login_required
@role_required('SUPER_ADMIN', 'ORG_ADMIN', 'HR_MANAGER', 'FINANCE_MANAGER', 'DEPT_MANAGER')
def executive_analytics_view(request):
    org = request.tenant_org
    analytics = AnalyticsService.get_executive_summary(org)
    reports = ScheduledReport.objects.filter(organization=org)
    
    # Format Chart.js payloads
    dept_labels = [d['name'] for d in analytics['dept_breakdown']]
    dept_data = [d['headcount'] for d in analytics['dept_breakdown']]
    
    gender_labels = [g['gender'] for g in analytics['gender_stats']]
    gender_data = [g['count'] for g in analytics['gender_stats']]
    
    return render(request, 'analytics/executive_dashboard.html', {
        'analytics': analytics,
        'reports': reports,
        'dept_labels_json': json.dumps(dept_labels),
        'dept_data_json': json.dumps(dept_data),
        'gender_labels_json': json.dumps(gender_labels),
        'gender_data_json': json.dumps(gender_data),
    })
