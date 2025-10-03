from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from django.core.cache import cache

from messaging.models import Message

@cache_page(60)  # Cache for 60 seconds
@require_GET
@login_required
def conversation_messages(request, other_user_id):
    """
    Display messages between the current user and another user.
    This view is cached for 60 seconds to improve performance.
    """
    messages = (
        Message.objects.filter(
            # Get messages where current user is either sender or receiver
            # and other user is the opposite
            (
                models.Q(sender=request.user, receiver_id=other_user_id) |
                models.Q(receiver=request.user, sender_id=other_user_id)
            )
        )
        .select_related('sender', 'receiver')
        .prefetch_related('replies')
        .order_by('-sent_at')
    )
    
    data = [
        {
            'message_id': str(msg.message_id),
            'sender': msg.sender.username,
            'receiver': msg.receiver.username,
            'content': msg.content,
            'sent_at': msg.sent_at.isoformat(),
            'read': msg.read,
            'has_replies': msg.replies.exists(),
        }
        for msg in messages
    ]
    
    return JsonResponse({
        'conversation': data,
        'cached_at': request.META.get('HTTP_IF_NONE_MATCH', '')  # Include cache info
    })

@require_POST
@login_required
def send_message(request, other_user_id):
    """
    Send a new message to another user.
    This view invalidates the conversation cache when a new message is sent.
    """
    content = request.POST.get('content')
    if not content:
        return JsonResponse({'error': 'Content is required'}, status=400)
    
    message = Message.objects.create(
        sender=request.user,
        receiver_id=other_user_id,
        content=content
    )
    
    # Invalidate the cached conversation
    cache_key = f'conversation:{request.user.id}:{other_user_id}'
    cache.delete(cache_key)
    cache_key_reverse = f'conversation:{other_user_id}:{request.user.id}'
    cache.delete(cache_key_reverse)
    
    return JsonResponse({
        'message_id': str(message.message_id),
        'status': 'sent'
    })

@cache_page(60)
@require_GET
@login_required
def recent_conversations(request):
    """
    Get a list of recent conversations for the current user.
    This view is cached for 60 seconds.
    """
    recent_messages = (
        Message.objects.filter(
            models.Q(sender=request.user) | models.Q(receiver=request.user)
        )
        .select_related('sender', 'receiver')
        .order_by('sender', 'receiver', '-sent_at')
        .distinct('sender', 'receiver')
    )
    
    conversations = []
    seen_pairs = set()
    
    for msg in recent_messages:
        other_user = msg.receiver if msg.sender == request.user else msg.sender
        pair = tuple(sorted([request.user.id, other_user.id]))
        
        if pair not in seen_pairs:
            seen_pairs.add(pair)
            conversations.append({
                'other_user': {
                    'id': other_user.id,
                    'username': other_user.username
                },
                'last_message': {
                    'content': msg.content,
                    'sent_at': msg.sent_at.isoformat(),
                    'is_read': msg.read
                }
            })
    
    return JsonResponse({
        'conversations': conversations,
        'cached_at': request.META.get('HTTP_IF_NONE_MATCH', '')
    })
