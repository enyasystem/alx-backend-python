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
    unread_count = Message.unread.unread_count_for_user(user)
    
    data = [
        {
            'message_id': str(m.message_id),
            'sender': getattr(m.sender, 'username', None),
            'content': m.content,
            'sent_at': m.sent_at.isoformat(),
            'parent_id': str(m.parent_message.message_id) if m.parent_message else None,
            'has_replies': bool(m.replies.all()),  # prefetched, so no extra query
        }
        for m in qs
    ]
    return JsonResponse({
        'unread': data,
        'total_unread': unread_count
    })

@require_POST
@login_required
def mark_messages_read(request):
    """Mark multiple messages as read."""
    message_ids = request.POST.getlist('message_ids[]')
    if not message_ids:
        return JsonResponse({'error': 'No message IDs provided'}, status=400)
        
    updated_count = Message.unread.mark_as_read(message_ids, request.user)
    
    return JsonResponse({
        'status': 'success',
        'marked_as_read': updated_count
    })


User = get_user_model()


@require_POST
@login_required
def delete_user(request):
    user = request.user
    # delete user will trigger post_delete signal
    user.delete()
    return JsonResponse({'status': 'deleted'})


@require_POST
@login_required
def send_message(request):
    """Send a new message to a specific user."""
    receiver_id = request.POST.get('receiver_id')
    content = request.POST.get('content')
    parent_id = request.POST.get('parent_id')  # Optional, for replies
    
    try:
        receiver = User.objects.get(pk=receiver_id)
        parent = Message.objects.get(pk=parent_id) if parent_id else None
        
        message = Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content,
            parent_message=parent
        )
        
        return JsonResponse({
            'status': 'success',
            'message_id': str(message.message_id)
        })
    except User.DoesNotExist:
        return JsonResponse({'error': 'Receiver not found'}, status=404)
    except Message.DoesNotExist:
        return JsonResponse({'error': 'Parent message not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_GET
@login_required
def list_messages(request):
    """List messages for the current user with optimized querying."""
    messages = (
        Message.objects.filter(receiver=request.user)
        .select_related('sender', 'parent_message')
        .prefetch_related('replies')
        .order_by('-sent_at')
    )
    
    data = [
        {
            'message_id': str(msg.message_id),
            'sender': msg.sender.username,
            'content': msg.content,
            'sent_at': msg.sent_at.isoformat(),
            'has_replies': msg.replies.exists(),
            'parent_id': str(msg.parent_message.message_id) if msg.parent_message else None
        }
        for msg in messages
    ]
    
    return JsonResponse({'messages': data})

@require_GET
@login_required
def threaded_message(request, message_id):
    """Return a message and its replies in a threaded nested structure.

    This view optimizes DB access by selecting related sender and prefetching
    all replies for the subtree in a single query, then builds the thread
    in-memory to avoid N+1 queries.
    """
    # Perform an optimized fetch here (select_related + prefetch_related)
    # Fetch the root message
    root = (
        Message.objects
        .select_related('sender')
        .prefetch_related('replies__sender')
        .only('message_id', 'content', 'sent_at', 'sender__username', 'parent_message')
        .get(message_id=message_id)
    )

    # Recursive ORM approach: repeatedly query children where parent in current_ids
    all_nodes = {root.message_id: root}
    current_ids = [root.pk]
    while current_ids:
        children_qs = (
            Message.objects
            .select_related('sender')
            .filter(parent_message__pk__in=current_ids)
            .only('message_id', 'content', 'sent_at', 'sender__username', 'parent_message')
        )
        children = list(children_qs)
        if not children:
            break
        for c in children:
            all_nodes[c.message_id] = c
        current_ids = [c.pk for c in children]

    # Build parent->children map
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
