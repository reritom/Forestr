from functools import wraps
from backend.models.profile import Profile
from backend.tools.response_tools import not_found, not_logged_in, not_permitted

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

class Assert:
    @classmethod
    def that(cls, object_representation: str):
        instance = cls()
        instance.object_representation_a = object_representation
        return instance

    def equals(self, other_object_representation: str):
        self.object_representation_b = other_object_representation
        return self

    def __call__(self, func):
        wraps(func)
        def inner(*args, **kwargs):
            kwarg_name_a, kwarg_a_attributes = Assert.parse_object_representation(self.object_representation_a)
            object_a_base = kwargs[kwarg_name_a]
            object_a = Assert.get_nested_attribute(object_a_base, kwarg_a_attributes)

            kwarg_name_b, kwarg_b_attributes = Assert.parse_object_representation(self.object_representation_b)
            object_b_base = kwargs[kwarg_name_b]
            object_b = Assert.get_nested_attribute(object_b_base, kwarg_b_attributes)

            if not object_a == object_b:
                return not_permitted(f"{self.object_representation_a} does not match {self.object_representation_b}")

            return func(*args, **kwargs)
        return inner

    @staticmethod
    def parse_object_representation(object_representation):
        kwarg_name, *nested_attributes = object_representation.split('.')
        return kwarg_name, nested_attributes

    @staticmethod
    def get_nested_attribute(base, attribute_tuple):
        obj = base
        for attribute in attribute_tuple:
            obj = getattr(obj, attribute)
        return obj


def attach_profile(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        # Retrieve or create a profile
        user = request.user
        profile = Profile.objects.get_or_create(user=user)[0]

        return func(request, *args, profile=profile, **kwargs)
    return inner

def login_required(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return not_logged_in()
        return func(request, *args, **kwargs)
    return inner
