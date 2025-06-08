# chats/middleware.py

from datetime import datetime, time
from django.http import HttpResponseForbidden

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now().time()
        allowed_start = time(18, 0)  # 6:00 PM
        allowed_end = time(21, 0)    # 9:00 PM

        if not (allowed_start <= current_time <= allowed_end):
            return HttpResponseForbidden("Access to the chat is only allowed between 6 PM and 9 PM.")

        return self.get_response(request)

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Track IPs and their message timestamps
        self.message_log = {}

    def __call__(self, request):
        # Only apply to POST requests to the messages endpoint
        if request.method == 'POST' and '/messages' in request.path:
            ip = self.get_client_ip(request)
            now = datetime.now()
            window_start = now - timedelta(minutes=1)

            # Initialize or clean up old timestamps
            timestamps = self.message_log.get(ip, [])
            timestamps = [ts for ts in timestamps if ts > window_start]
            timestamps.append(now)
            self.message_log[ip] = timestamps

            if len(timestamps) > 5:
                return HttpResponseForbidden("Rate limit exceeded: Max 5 messages per minute per IP.")

        return self.get_response(request)
        
class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Example: Only restrict actions under /api/conversations/ and /api/messages/
        protected_paths = ['/api/conversations/', '/api/messages/']

        if any(request.path.startswith(path) for path in protected_paths):
            if request.user.is_authenticated:
                user_role = getattr(request.user, 'role', None)
                if user_role not in ['admin', 'moderator']:
                    return HttpResponseForbidden("Access denied: insufficient role permissions.")
            else:
                return HttpResponseForbidden("Authentication required.")

        return self.get_response(request)
    def get_client_ip(self, request):
        """Handles getting client IP even behind a proxy."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
