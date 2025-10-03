from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET


from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET

from .models import Message


@require_GET
@login_required
def unread_inbox(request):
    user = request.user
    # Use the custom manager to fetch unread messages optimized with select_related() and only()
    qs = Message.unread.unread_for_user(user)
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


@require_GET
@login_required
def threaded_message(request, message_id):
    """Return a message and its replies in a threaded nested structure.

    This view optimizes DB access by selecting related sender and prefetching
    all replies for the subtree in a single query, then builds the thread
    in-memory to avoid N+1 queries.
    """
    # Delegate thread assembly to the manager to keep view logic thin
    thread = Message.unread.thread_for_message(message_id)
    return JsonResponse({'thread': thread})
