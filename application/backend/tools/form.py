from collections import defaultdict
from datetime import datetime
from django.db import models

class Form:
    def __init__(self, model):
        self._model = model
        self._converter = defaultdict(lambda value: value, {
            models.CharField: lambda value: str(value),
            models.BooleanField: lambda value: value in ['true', 'True', 'y', 'Y', 1, True],
            models.IntegerField: lambda value: int(value),
            models.DateTimeField: lambda value: value if isinstance(value, datetime) else datetime.fromisoformat(value)
        })

    @classmethod
    def for_model(cls, model):
        instance = cls(model)
        return instance

    def with_request(self, request):
        self.__dict__.update({
            key: value[0]
            for key, value
            in request.POST.lists()
        })

        self._convert_types()
        return self

    def _convert_types(self):
        definitions = {
            definition.name: definition.__class__
            for definition
            in self._model._meta.fields
        }

        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                if key in definitions:
                    try:
                        #print(f"Converting {key}")
                        self.__dict__[key] = self._converter[definitions[key]](value)
                    except Exception as e:
                        print(f"Failed to convert value from type {type(self.__dict__[key])} in form construction")



    def __getattr__(self, key):
        return None
