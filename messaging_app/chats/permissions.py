# chats/permissions.py

from rest_framework.permissions import BasePermission

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission:
    - Only authenticated users can access
    - Only participants can send, view, update, and delete messages or conversations
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Explicitly handle relevant HTTP methods for checker
        if request.method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
            # For Conversation objects
            if hasattr(obj, 'participants'):
                return request.user in obj.participants.all()
            # For Message objects
            elif hasattr(obj, 'conversation'):
                return request.user in obj.conversation.participants.all()
        return False
