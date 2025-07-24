from rest_framework import serializers
from chats.models import User, Conversation, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only =True,min_length=8)

    class Meta:
        model= User
        fields=['user_id','email','username','first_name','last_name','phone_number','password']
        read_only_fields=['user_id']
    def validate_email(self,value):
        if not value.endswith('@gmail.com'):
            raise serializers.ValidationError("Only Gmail addresses are allowed.")
        return value
    def create(self,validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
       
        return user

# this serilaizer is for displaying users information 
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['user_id', 'email', 'username', 'full_name']
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def validate_email(self, value):
        if not value.endswith('@gmail.com'):
            raise serializers.ValidationError("Only Gmail addresses are allowed.")
        return value

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at','conversion']

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']
