from functools import wraps
from backend.tools.response_tools import not_found

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
