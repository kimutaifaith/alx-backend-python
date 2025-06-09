from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Message
from django.shortcuts import render
from .serializers import MessageSerializer
from rest_framework.views import APIView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class UnreadMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get unread messages using the custom manager method
        unread_messages_qs = Message.unread.unread_for_user(request.user)

        # Further optimize by specifying only necessary fields in the view (optional)
        unread_messages_qs = unread_messages_qs.only('id', 'sender', 'content', 'timestamp')

        serializer = MessageSerializer(unread_messages_qs, many=True)
        return Response(serializer.data)
@login_required
def delete_user(request):
    if request.method == "POST":
        request.user.delete()
        return redirect('account_deleted')  # Replace with your redirect URL
    return redirect('profile')  # Or any page if method is not POST

def get_message_thread(message):
    thread = []

    def fetch_replies(msg):
        replies = msg.replies.all().select_related('sender', 'receiver')
        for reply in replies:
            reply_data = {
                'id': reply.id,
                'sender': reply.sender.username,
                'receiver': reply.receiver.username,
                'content': reply.content,
                'timestamp': reply.timestamp,
                'replies': []
            }
            reply_data['replies'] = fetch_replies(reply)
            thread.append(reply_data)
        return thread

    return fetch_replies(message)


@login_required
def inbox(request):
    # ✅ sender = request.user
    messages = (
        Message.objects.filter(receiver=request.user)
        .select_related('sender', 'receiver', 'parent_message')
        .order_by('-timestamp')
    )
    return render(request, 'messaging/inbox.html', {'messages': messages})

@login_required
def send_message(request):
    if request.method == 'POST':
        receiver_username = request.POST.get('receiver')
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')  # optional

        try:
            receiver = User.objects.get(username=receiver_username)
        except User.DoesNotExist:
            return render(request, 'messaging/send.html', {'error': 'User not found'})

        parent_message = Message.objects.filter(id=parent_id).first() if parent_id else None

        # ✅ Create new message with sender=request.user
        Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content,
            parent_message=parent_message
        )
        return render(request, 'messaging/send.html', {'success': 'Message sent!'})

    return render(request, 'messaging/send.html')

@login_required
def unread_inbox(request):
    unread_messages = Message.unread.for_user(request.user).select_related('sender')
    return render(request, 'messaging/unread_inbox.html', {'messages': unread_messages})

@method_decorator(cache_page(60), name='dispatch')  # Cache for 60 seconds
class MessageListView(APIView):
    def get(self, request, conversation_id):
        messages = Message.objects.filter(conversation_id=conversation_id).order_by('timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)