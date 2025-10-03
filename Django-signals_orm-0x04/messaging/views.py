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
    # Perform an optimized fetch here (select_related + prefetch_related)
    root = (
        Message.objects
        .select_related('sender')
        .prefetch_related('replies__sender', 'replies__replies__sender', 'replies__replies__replies__sender')
        .only('message_id', 'content', 'sent_at', 'sender__username', 'parent_message')
        .get(message_id=message_id)
    )

    # Walk prefetched replies to build the threaded structure without extra queries
    all_nodes = {root.message_id: root}

    def walk(node):
        for child in getattr(node, 'replies').all():
            all_nodes[child.message_id] = child
            walk(child)

    walk(root)

    children_map = {}
    for node in all_nodes.values():
        pid = getattr(node.parent_message, 'message_id', None)
        children_map.setdefault(pid, []).append(node)

    def build_node(msg):
        node = {
            'message_id': str(msg.message_id),
            'sender': getattr(msg.sender, 'username', None),
            'content': msg.content,
            'sent_at': msg.sent_at.isoformat(),
            'replies': [],
        }
        for child in children_map.get(msg.message_id, []):
            if child.message_id == msg.message_id:
                continue
            node['replies'].append(build_node(child))
        return node

    thread = build_node(root)
    return JsonResponse({'thread': thread})
