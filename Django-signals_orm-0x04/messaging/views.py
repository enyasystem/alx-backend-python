from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET


@require_GET
@login_required
def unread_inbox(request):
    user = request.user
    # Use the custom manager to fetch unread messages optimized with only()
    qs = request.user.received_messages.model.unread.unread_for(user)
    data = [
        {
            'message_id': str(m.message_id),
            'sender': getattr(m.sender, 'username', None),
            'content': m.content,
            'sent_at': m.sent_at.isoformat(),
        }
        for m in qs
    ]
    return JsonResponse({'unread': data})


User = get_user_model()


@require_POST
@login_required
def delete_user(request):
    user = request.user
    # delete user will trigger post_delete signal
    user.delete()
    return JsonResponse({'status': 'deleted'})
