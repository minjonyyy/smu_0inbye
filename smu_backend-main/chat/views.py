from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Count
from .models import ChatRoom, ChatMessage
from .serializers import ChatRoomSerializer, ChatMessageSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model

User = get_user_model()

def get_email_prefix(email):
    return email.split('@')[0]

class CreateChatRoomAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        sender = request.user
        recipient_email_prefix = get_email_prefix(username)
        recipient = get_object_or_404(User, email__startswith=recipient_email_prefix)

        # 발신자와 수신자가 동일한 경우 채팅방 생성 방지
        if sender.email == recipient.email:
            print(f"자기 자신과의 채팅방은 생성할 수 없습니다.")
            return Response({"detail": "자기 자신과의 채팅방은 생성할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        room = ChatRoom.objects.annotate(participant_count=Count('participants')).filter(
            participants=sender
        ).filter(participants=recipient).first()

        if room:
            print(f"기존 채팅방이 확인되었습니다: {room.id}")
            return Response({"room_exists": True, "id": room.id}, status=status.HTTP_200_OK)
        else:
            room = ChatRoom.objects.create()
            room.participants.add(sender, recipient)
            print(f"새로운 채팅방이 생성되었습니다: {room.id}")

        serializer = ChatRoomSerializer(room)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SendMessageAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, room_id):
        sender = request.user

        room = get_object_or_404(ChatRoom, id=room_id)
        if sender not in room.participants.all():
            return Response({"detail": "해당 채팅방에 접근할 수 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        message = request.data.get('message')
        chat_message = ChatMessage.objects.create(room=room, sender=sender, message=message)
        serializer = ChatMessageSerializer(chat_message)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{room.id}",
            {
                "type": "chat_message",
                "message": message,
                "sender_email": sender.email,
            }
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

class ChatRoomAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_id):
        room = get_object_or_404(ChatRoom, id=room_id)
        serializer = ChatRoomSerializer(room)
        return Response(serializer.data)

class ChatMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_id):
        room = get_object_or_404(ChatRoom, id=room_id)
        messages = ChatMessage.objects.filter(room=room)
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)
    

class ChatRoomListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        chat_rooms = ChatRoom.objects.filter(participants=user)

        if not chat_rooms.exists():
            return Response({"detail": "참여 중인 채팅방이 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        chat_rooms_data = []
        for room in chat_rooms:
            participants = room.participants.exclude(id=user.id)  # 현재 사용자를 제외한 참가자
            for participant in participants:
                chat_rooms_data.append({
                    "id": room.id,
                    "participant_email": participant.email,
                    "participant_username": get_email_prefix(participant.email) 
                })

        return Response(chat_rooms_data, status=status.HTTP_200_OK)


class CheckChatRoomAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        sender = request.user
        recipient_email_prefix = get_email_prefix(username)
        print(f"수신자: {username}")

        # 수신자 정보 조회
        try:
            recipient = get_object_or_404(User, email__startswith=recipient_email_prefix)
        except Exception as e:
            return Response({"detail": "해당 사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        # 자기 자신과의 채팅방 생성을 방지
        if sender == recipient:
            return Response({"detail": "자기 자신과의 채팅방은 생성할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 기존 방 확인
        room = ChatRoom.objects.annotate(participant_count=Count('participants')).filter(
            participant_count=2,
            participants=sender
        ).filter(participants=recipient).first()

        if room:
            print(f"{room.id}번 채팅방 with {username}")
            return Response({"room_exists": True, "id": room.id}, status=status.HTTP_200_OK)
        else:
            return Response({"room_exists": False}, status=status.HTTP_200_OK)


class CheckChatRoomByIdAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_id):
        sender = request.user
        # room_id가 있고, sender가 참가자 중 하나로 속한 채팅방을 가져옵니다.
        room = get_object_or_404(ChatRoom, id=room_id, participants=sender)

        return Response({"room_exists": True, "id": room.id}, status=status.HTTP_200_OK)