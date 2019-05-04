from functools import wraps
from backend.models.profile import Profile
from backend.tools.response_tools import not_found, not_logged_in

class Attach:
    @classmethod
    def incoming(cls, function_keyword):
        instance = cls()
        instance.function_keyword = function_keyword
        return instance

    def to(self, model):
        self.model = model
        return self

    def as_outgoing(self, new_function_keyword):
        self.new_function_keyword = new_function_keyword
        return self

    def __call__(self, func):
        wraps(func)
        def inner(*args, **kwargs):
            if self.function_keyword in kwargs:
                try:
                    model_instance = self.model.objects.get(id=kwargs[self.function_keyword])
                except:
                    return not_found(f"Nothing found for parameter {self.function_keyword} with value {kwargs[self.function_keyword]}")

                kwargs[self.new_function_keyword] = model_instance
                kwargs.pop(self.function_keyword)
            return func(*args, **kwargs)
        return inner

def attach_profile(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        # Retrieve or create a profile
        user = request.user
        profile = Profile.objects.get_or_create(user=user)[0]

        return func(request, profile, *args, **kwargs)
    return inner

def login_required(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return not_logged_in()
        return func(request, *args, **kwargs)
    return inner
