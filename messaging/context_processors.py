from messaging.models import MessageStatus, Message


def messaging_context(request):
    messaging_context = {}
    if hasattr(request, 'user') and request.user.id is not None:
        unread_count = Message.objects.filter(recipient=request.user, status=MessageStatus.UNREAD).count()
        messaging_context = {
            'unread_count': unread_count
        }
    return {
        'message_context': messaging_context
    }


