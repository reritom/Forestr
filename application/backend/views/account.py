from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import uuid

from backend.models.profile import Profile
from backend.models.organisation import Organisation
from backend.tools.response_tools import (
    ok,
    not_logged_in,
    conflict,
    method_not_allowed,
    not_found,
    internal_error
)

@csrf_exempt
def signup(request):
    if request.user.is_authenticated:
        return conflict("Already logged in")

    if request.method == 'POST':
        if User.objects.filter(username=request.POST['username']).exists():
            return conflict("This username already exists")

        user = User.objects.create_user(
            username=request.POST['username'],
            email=request.POST['email'],
            password=request.POST['password']

        )

        organisation = Organisation.make(
            owner=user,
            personal=True,
            enterprise=False,
            name=str(uuid.uuid4()),
            description="Personal organisation"
        )

        profile = Profile.objects.create(
            user=user,
            organisation=organisation,
            moderator=True
        )

        login(request, user)
        return ok({'message':'User account successfully created'})
    else:
        return method_not_allowed()

@csrf_exempt
def login_user(request):
    if request.method == 'GET':
        return ok({'logged_in': request.user.is_authenticated()})

    elif request.method == 'POST':
        if request.user.is_authenticated:
            return ok({'logged_in': request.user.is_authenticated()})

        if not User.objects.filter(username=request.POST['username']).exists():
            return not_found("Username doesn't exist")

        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user:
            login(request, user)
            return ok({'message':'User successfully logged in'})
        else:
            return internal_error("Unsuccessful login")

    else:
        return method_not_allowed()

def logout_user(request):
     logout(request)
     return ok({'message':'User successfully logged out'})
