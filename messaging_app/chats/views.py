from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user).distinct()

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['conversation']
    search_fields = ['content']
    ordering_fields = ['timestamp']
    filterset_class = MessageFilter
    pagination_class = MessagePagination

    def get_queryset(self):
        conversation_id = self.request.query_params.get('conversation')
        if conversation_id:
            return Message.objects.filter(
                conversation_id=conversation_id,
                conversation__participants=self.request.user
            )
        return Message.objects.none()

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get("conversation")
        if self.request.user not in conversation.participants.all():
            return Response({"error": "You are not a participant in this conversation."},
                            status=status.HTTP_403_FORBIDDEN)
        serializer.save(sender=self.request.user)