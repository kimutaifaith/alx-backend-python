# chats/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly, IsParticipantOfConversation
from django_filters.rest_framework import DjangoFilterBackend
from .filters import MessageFilter


from .models import Conversation, Message, CustomUser
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, IsParticipantOfConversation]

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

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        serializer.save(participants=[self.request.user])


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter
    
        
    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get('conversation_id')
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("HTTP_403_FORBIDDEN: You are not a participant in this conversation.")
        serializer.save(sender=self.request.user)