from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framwork import permissions

class IsAuthenticatedAndParticipant(BasePermission):
    def has_permission(self,request,view):
        return request.user and request.user.is_authenticated
    def has_object_permission(self,request,view,obj):
        return request.user in obj.participants.all()

