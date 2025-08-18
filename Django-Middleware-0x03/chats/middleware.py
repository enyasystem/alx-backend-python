import time
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden, JsonResponse
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

# Simple in-memory store for rate limiting (IP -> [timestamps])
_rate_store = defaultdict(list)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logfile = 'requests.log'

    def __call__(self, request):
        user = getattr(request, 'user', 'Anonymous')
        entry = f"{datetime.now()} - User: {user} - Path: {request.path}\n"
        with open(self.logfile, 'a', encoding='utf-8') as f:
            f.write(entry)
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()
        # allow between 06:00 and 21:00
        start = datetime.strptime('06:00', '%H:%M').time()
        end = datetime.strptime('21:00', '%H:%M').time()
        if not (start <= now <= end):
            return HttpResponseForbidden('Chat access allowed only between 06:00 and 21:00')
        return self.get_response(request)

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.limit = 5  # messages per minute
        self.window = timedelta(minutes=1)

    def __call__(self, request):
        if request.method == 'POST' and request.path.endswith('/messages/'):
            ip = request.META.get('REMOTE_ADDR', 'unknown')
            now = time.time()
            timestamps = _rate_store[ip]
            # remove old
            _rate_store[ip] = [ts for ts in timestamps if now - ts < self.window.total_seconds()]
            if len(_rate_store[ip]) >= self.limit:
                return JsonResponse({'error': 'Rate limit exceeded'}, status=429)
            _rate_store[ip].append(now)
        return self.get_response(request)

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only enforce on admin routes under /admin/ or /chats/admin/
        if request.path.startswith('/chats/admin/') or request.path.startswith('/admin/'):
            user = getattr(request, 'user', None)
            if not user or not getattr(user, 'is_authenticated', False):
                return HttpResponseForbidden('Authentication required')
            role = getattr(user, 'role', None)
            if role not in ('admin', 'host'):
                return HttpResponseForbidden('Admin or host role required')
        return self.get_response(request)
