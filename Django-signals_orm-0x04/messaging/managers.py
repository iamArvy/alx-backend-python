from django.db import models
from django.db.models import Q, Prefetch
from .models import Message

class MessageManager(models.Manager):
    def get_user_conversations(self, user):
        """Optimized query for user's conversations"""
        return self.filter(
            Q(sender=user) | Q(receiver=user),
            parent_message__isnull=True
        ).select_related(
            'sender', 'receiver'
        ).prefetch_related(
            Prefetch(
                'replies',
                queryset=Message.objects.select_related(
                    'sender', 'receiver'
                ).order_by('timestamp')
            )
        ).order_by('-timestamp')
    
class UnreadMessagesManager(models.Manager): 
    def unread_for_user(self, user):
        """Explicitly named method for unread messages"""
        return self.filter(
            receiver=user,
            is_read=False
        ).select_related('sender').only(
            'id',
            'content',
            'timestamp',
            'sender__username',
            'parent_message_id'
        ).order_by('-timestamp')