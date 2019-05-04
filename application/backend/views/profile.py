from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from backend.models.profile import Profile
from backend.serialisers.profile_serialiser import ProfileSerialiser

from backend.tools.response_tools import (
    ok
)

@method_decorator(login_required, name="dispatch")
class ProfileView(View):
    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        return ok({
            'profile': ProfileSerialiser.serialise(profile)
        })
