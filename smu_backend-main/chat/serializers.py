# chat/serializers.py
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import ChatRoom, ChatMessage

User = get_user_model()  # 사용자 모델 가져오기

class ChatRoomSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = ChatRoom
        fields = ['id', 'participants']

class ChatMessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.EmailField(source="sender.email", read_only=True)  # 이메일 필드 추가
    room = serializers.PrimaryKeyRelatedField(queryset=ChatRoom.objects.all())

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'sender_email', 'room', 'message', 'timestamp']
