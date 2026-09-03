from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from .models import Notification
from .services import NotificationService

@login_required
def notification_list_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:30]
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    return render(request, 'notifications/list.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })

@login_required
def mark_read_view(request, notification_id):
    notif = NotificationService.mark_as_read(notification_id, request.user)
    if notif and notif.action_url:
        return redirect(notif.action_url)
    return redirect('notifications:list')

@login_required
def mark_all_read_view(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True, read_at=timezone.now())
    return redirect('notifications:list')
