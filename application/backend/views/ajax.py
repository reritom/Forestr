from backend.models.organisation import Organisation
from django.contrib.auth.models import User

def ajax_dispatch(request, resource):
    pass

def organisation_name_is_valid(request):
    return Organisation.objects.filter(name=request.POST['name']).exists()

def username_is_valid(request):
    return User.objects.filter(name=request.POST['username']).exists()

def email_is_valid(request):
    return User.objects.filter(email=request.POST['email']).exists()
