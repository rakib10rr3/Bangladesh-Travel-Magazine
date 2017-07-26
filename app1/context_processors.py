from .models import Notification


def notification(request):
    if hasattr(request, 'user'):
        user = request.user
        n = Notification.objects.filter(recipient_id=user.id, unread=True)
        total_notification = n.count()
    else:
        total_notification = 0

    return {
        'notification_count': total_notification,
    }
