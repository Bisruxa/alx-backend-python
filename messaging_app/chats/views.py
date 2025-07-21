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
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['participants__username']
    filterset_fields = ['participants']

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
       


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['text']
    filterset_fields = ['conversation', 'sender']

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        message = serializer.save(sender=self.request.user)
        