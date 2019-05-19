from backend.models.organisation import Organisation
from django.contrib.auth.models import User
from backend.tools.response_tools import ok, not_found

def ajax_dispatch(request, resource):
    router = {
        'username': username_is_valid,
        'organisation': organisation_name_is_valid,
        'email': email_is_valid
    }

    if not resouce in router:
        return not_found("Resource not found")

    return ok({'available': router.get(resource)(request)})

def organisation_name_is_valid(request):
    return Organisation.objects.filter(name=request.POST['name']).exists()

def username_is_valid(request):
    return User.objects.filter(name=request.POST['username']).exists()

def email_is_valid(request):
    return User.objects.filter(email=request.POST['email']).exists()
