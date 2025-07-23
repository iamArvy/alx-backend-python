# chats/filters.py

import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    # Filter by sender's user ID
    sender = django_filters.UUIDFilter(field_name='sender__user_id')

    # Filter messages by sent date range
    sent_after = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    sent_before = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'sent_after', 'sent_before']
