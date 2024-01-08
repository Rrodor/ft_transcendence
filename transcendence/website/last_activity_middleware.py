from django.utils import timezone
from django.contrib.auth import get_user_model

class LastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            User = get_user_model()
            user = User.objects.get(id=request.user.id)
            user.last_activity = timezone.now()
            user.save()
        return response
