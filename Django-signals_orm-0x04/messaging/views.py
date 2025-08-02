from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.cache import cache_page
# from django.utils.decorators import method_decorator
# from django.views import View
from .models import Message

User = get_user_model()

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        logout(request)  # Log out before deletion to avoid issues
        user.delete()  # This triggers the post_delete signal
        return HttpResponse(status=204)
    else:
        # Always return an HttpResponse, even if not POST
        return HttpResponse(status=405)


@login_required
def thread_view(request, message_id):
    # Get message with sender=request.user check
    message = get_object_or_404(
        Message.objects.filter(
            Q(sender=request.user) | Q(receiver=request.user)
        ).select_related('sender', 'receiver'),
        pk=message_id
    )
    return render(request, 'messaging/thread.html', {
        'root_message': message,
        'thread': message.get_thread()
    })

@login_required
def inbox_view(request):
    # Explicitly filter messages where user is sender or receiver
    conversations = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user),
        parent_message__isnull=True
    ).select_related(
        'sender', 'receiver'
    ).prefetch_related(
        'replies'
    ).order_by('-timestamp')
    
    return render(request, 'messaging/inbox.html', {
        'conversations': conversations
    })

@login_required
@require_GET
def unread_messages_api(request):
    """JSON API endpoint for unread messages with explicit optimizations"""
    # Using the custom manager with explicit field selection
    messages = Message.unread_messages.unread_for_user(request.user).only(
        'id',
        'content',
        'timestamp',
        'sender__username',
        'parent_message_id'
    )
    
    response_data = {
        'count': messages.count(),
        'messages': [
            {
                'id': msg.id,
                'sender': msg.sender.username,
                'content': msg.content,
                'timestamp': msg.timestamp.isoformat(),
                'is_reply': bool(msg.parent_message_id)
            }
            for msg in messages
        ]
    }
    
    return JsonResponse(response_data)

@login_required
@cache_page(60)  # Cache for 60 seconds
def cached_thread_view(request, thread_id):
    messages = Message.objects.filter(
        thread_id=thread_id
    ).select_related('sender').order_by('timestamp')
    
    data = {
        'messages': [
            {
                'id': msg.pk,
                'sender': msg.sender.username,
                'content': msg.content,
                'timestamp': msg.timestamp.isoformat()
            }
            for msg in messages
        ]
    }
    return JsonResponse(data)