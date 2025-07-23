# chats/permissions.py

from rest_framework import permissions

class IsParticipant(permissions.BasePermission):
    """
    Custom permission to check if the user is a participant in the conversation.
    Works for both Conversation and Message objects.
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'participants'):  # For Conversation
            return request.user in obj.participants.all()
        elif hasattr(obj, 'conversation'):  # For Message
            return request.user in obj.conversation.participants.all()
        return False
