from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer,RegisterSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken 
from rest_framework.permissions import AllowAny
from .permissions import IsAuthenticatedAndParticipant
from rest_framework.exceptions import PermissionDenied
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class RegisterView(APIView):
      
    permission_classes = [AllowAny]
    def post(self,request):

        serializer= RegisterSerializer(data = request.data)
        if serializer.is_valid():
            user= serializer.save()
            refresh= RefreshToken.for_user(user)
            return Response({
                "refresh":str(refresh),
                "access":str(refresh.access_token),
                "user":{
                    "user_id":str(user.user_id),
                    "email":user.email,
                    "username":user.username,
                    "first_name":user.first_name,
                    "last_name":user.last_name,
                    "phone_number":user.phone_number

                }
            },status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticatedAndParticipant]

    # filtering
    filter_backends =[DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields=['user','conversation']
    search_fileds=['user']
    ordering_fields=['created_at']
   
    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.save()
        if self.request.user not in conversation.participants.all():
            conversation.participants.add(self.request.user)

       


class MessageViewSet(viewsets.ModelViewSet):

    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticatedAndParticipant]
    

    # filtering
    filter_backends =[DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields=['user','conversation']
    search_fileds=['content']
    ordering_fields=['created_at']

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_id')
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            raise PermissionDenied(detail="Conversation not found")

        # Permission check
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied(detail="You are not a participant", code=status.HTTP_403_FORBIDDEN)

        return Message.objects.filter(conversation=conversation)

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get('conversation_id')
        conversation = Conversation.objects.get(id=conversation_id)
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied(detail="You are not a participant", code=status.HTTP_403_FORBIDDEN)
        serializer.save(user=self.request.user, conversation=conversation)
        