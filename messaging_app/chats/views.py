# chats/views.py

from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend

from .models import Conversation, Message, CustomUser
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user_ids = request.data.get('participants', [])
        if not user_ids or not isinstance(user_ids, list):
            return Response({"error": "Participants list is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            users = CustomUser.objects.filter(user_id__in=user_ids)
            if users.count() != len(user_ids):
                raise ValueError("One or more users not found.")
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        conversation.participants.set(users)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    # Add filtering support
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['conversation', 'sender']
    search_fields = ['message_body']

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
