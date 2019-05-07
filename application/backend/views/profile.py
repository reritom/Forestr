from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from backend.models.profile import Profile
from backend.tools.form import Form
from backend.serialisers.profile_serialiser import ProfileSerialiser

from backend.tools.decorators import login_required
from backend.tools.decorators import attach_profile
from backend.tools.response_tools import (
    ok
)

@method_decorator(login_required, name="dispatch")
@method_decorator(attach_profile, name="dispatch")
class ProfileView(View):
    def get(self, request, profile):
        return ok({
            'profile': ProfileSerialiser.serialise_with_organisation(profile)
        })

    def patch(self, request, profile):
        # Change the email, change the username, change the password
        # All require confirmations
        pass

    def delete(self, request, profile):
        # Deleting a profile requires email confirmation and will delete the personal organisation too,
        # If is in an enterprise organisation, it will leave,
        # If it owns an organisation, the organisation will be deleted
        pass
