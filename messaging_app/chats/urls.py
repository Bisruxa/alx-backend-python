from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet, RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Parent router for conversations
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Nested router for messages under a conversation
convo_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
convo_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),  
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    
    path('', include(router.urls)),        
    path('', include(convo_router.urls)),     
]
