from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied

class RestrictStaffToAdminMiddleware(MiddlewareMixin):
    """
    A middleware that restricts staff members access to administration panels.
    """
    def process_request(self, request):
        if request.path.startswith(reverse('admin:index')):
            if request.user.is_authenticated:
                if not request.user.is_staff:
                    raise PermissionDenied()
            else:
                raise PermissionDenied()