from rest_framework.permissions import BasePermission, IsAuthenticated

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to allow only participants in a conversation
    to send, view, update, and delete messages or conversations.
    """

    def has_permission(self, request, view):
        # Only allow access if the user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check if the object is a conversation
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        # Check if the object is a message
        elif hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
        return False
