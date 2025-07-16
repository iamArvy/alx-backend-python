from django.urls import path, include
from rest_framework_nested import routers
from .views import ConversationViewSet, MessageViewSet, UserViewSet

# Root router for users
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# Nested: users/{user_id}/conversations/
users_router = routers.NestedDefaultRouter(router, r'users', lookup='user')
users_router.register(r'conversations', ConversationViewSet, basename='user-conversations')

# Nested: users/{user_id}/conversations/{conversation_id}/messages/
conversation_router = routers.NestedDefaultRouter(users_router, r'conversations', lookup='conversation')
conversation_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# Final URL patterns
urlpatterns = router.urls + users_router.urls + conversation_router.urls
