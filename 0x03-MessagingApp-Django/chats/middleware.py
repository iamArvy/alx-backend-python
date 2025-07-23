import logging
from datetime import datetime, time as dtime
from django.http import HttpResponseForbidden
import time
from collections import defaultdict, deque
from django.http import JsonResponse

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('request_logger')
        handler = logging.FileHandler('request_logs.log')
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)

        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = dtime(18, 0)  # 6:00 PM
        end_time = dtime(21, 0)    # 9:00 PM
        current_time = datetime.now().time()

        if request.path.startswith('/messaging/'):
            if not (start_time <= current_time <= end_time):
                return HttpResponseForbidden("Access to the messaging app is only allowed between 6PM and 9PM.")

        response = self.get_response(request)
        return response

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_logs = defaultdict(deque)  # Store timestamps for each IP

        self.MESSAGE_LIMIT = 5
        self.TIME_WINDOW = 60  # seconds

    def __call__(self, request):
        if request.path.startswith('/messaging/') and request.method == 'POST':
            ip = self.get_client_ip(request)
            now = time.time()

            message_times = self.message_logs[ip]

            # Remove timestamps older than TIME_WINDOW
            while message_times and now - message_times[0] > self.TIME_WINDOW:
                message_times.popleft()

            if len(message_times) >= self.MESSAGE_LIMIT:
                return JsonResponse({
                    "error": "Rate limit exceeded. Only 5 messages allowed per minute."
                }, status=429)

            message_times.append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        # Check for forwarded IP first
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')