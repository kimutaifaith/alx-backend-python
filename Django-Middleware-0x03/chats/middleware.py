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
