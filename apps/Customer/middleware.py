
from django.utils.deprecation import MiddlewareMixin

class DisableCSRFCheckMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Disable CSRF check for requests starting with /api/
        if request.path.startswith('/api/'):
            setattr(request, '_dont_enforce_csrf_checks', True)
