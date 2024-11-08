# chat/urls.py
from django.urls import path
from .views import SendMessageAPI, CreateChatRoomAPI, ChatRoomAPI, ChatMessageView, ChatRoomListAPI, CheckChatRoomAPI, CheckChatRoomByIdAPI

urlpatterns = [
    path('send/<int:room_id>/', SendMessageAPI.as_view(), name='send_message'),
    path('create-room/<str:username>/', CreateChatRoomAPI.as_view(), name='create_chat_room'),
    path('room/<int:room_id>/', ChatRoomAPI.as_view(), name='chat_room'),
    path('messages/<int:room_id>/', ChatMessageView.as_view(), name='chat_messages'),
    path('list/', ChatRoomListAPI.as_view(), name='chat_room_list'),
    path('check-room/<str:username>/', CheckChatRoomAPI.as_view(), name='check_chat_room'),
    path('check-room-by-id/<int:room_id>/', CheckChatRoomByIdAPI.as_view(), name='check_chat_room_by_id'),
]
