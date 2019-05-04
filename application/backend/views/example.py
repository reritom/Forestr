from backend.models.example import Example

from django.http import JsonResponse

def example_view(request):
    return JsonResponse({})
