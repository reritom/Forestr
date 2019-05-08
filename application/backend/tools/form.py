from collections import defaultdict
from datetime import datetime
from django.db import models
from django.http import QueryDict

class Form:
    def __init__(self, model=None):
        self._model = model
        self._converter = defaultdict(lambda: lambda value: value, {
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
        if request.method == 'POST':
            self.__dict__.update({
                key: value[0]
                for key, value
                in request.POST.lists()
            })
        else:
            self.__dict__.update({
                key: value
                for key, value
                in QueryDict(request.body)
            })

        if self._model:
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
                        print(f"Failed to convert value {self.__dict__[key]} from type {type(self.__dict__[key])} to {definitions[key]} in form construction")



    def __getattr__(self, key):
        return None
