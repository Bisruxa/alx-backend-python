from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]




# from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
# from .views import ConversationViewSet, MessageViewSet

# router = DefaultRouter()
# router.register(r'conversations', ConversationViewSet, basename='conversation')

# convo_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
# convo_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# urlpatterns = [
#     path('', include(router.urls)),
#     path('', include(convo_router.urls)),
# ]