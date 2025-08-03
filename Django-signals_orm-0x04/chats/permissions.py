from rest_framework import permissions
from .models import Conversation

class IsAuthenticatedAndParticipant(permissions.BasePermission):
    def has_permission(self,request,view):
        return request.user and request.user.is_authenticated
    def has_object_permission(self,request,view,obj):
        if not request.user.is_authenticated:
            return False

        if hasattr(obj, 'conversation'):
            is_participant = request.user in obj.conversation.participants.all()
        elif isinstance(obj, Conversation):
            is_participant = request.user in obj.participants.all()
        else:
            return False

        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return is_participant
        return True

