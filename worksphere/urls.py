from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('organizations/', include('apps.organizations.urls')),
    path('employees/', include('apps.employees.urls')),
    path('recruitment/', include('apps.recruitment.urls')),
    path('onboarding/', include('apps.onboarding.urls')),
    path('attendance/', include('apps.attendance.urls')),
    path('shifts/', include('apps.shifts.urls')),
    path('leaves/', include('apps.leave_management.urls')),
    path('holidays/', include('apps.holidays.urls')),
    path('compensation/', include('apps.compensation.urls')),
    path('payroll/', include('apps.payroll.urls')),
    path('benefits/', include('apps.benefits.urls')),
    path('expenses/', include('apps.expenses.urls')),
    path('travel/', include('apps.travel.urls')),
    path('performance/', include('apps.performance.urls')),
    path('learning/', include('apps.learning.urls')),
    path('assets/', include('apps.assets.urls')),
    path('documents/', include('apps.documents.urls')),
    path('helpdesk/', include('apps.helpdesk.urls')),
    path('analytics/', include('apps.analytics.urls')),
    path('notifications/', include('apps.notifications.urls')),
    path('audit/', include('apps.audit.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
