from django.http import JsonResponse

def internal_error(buffer: str):
    return JsonResponse({'message': buffer}, status=500)

def not_found(buffer: str):
    return JsonResponse({'message': buffer}, status=404)

def not_logged_in(buffer: str):
    return JsonResponse({'message': buffer}, status=401)

def not_permitted(buffer: str):
    return JsonResponse({'message': buffer}, status=403)

def method_not_allowed():
    return JsonResponse({'message': "Unsupported request method"}, status=405)

def conflict(buffer: str):
    return JsonResponse({'message': buffer}, status=409)

def ok(response: dict):
    return JsonResponse(response, status=200)

def created(response: dict):
    return JsonResponse(response, status=201)

def accepted(response: dict):
    return JsonResponse(response, status=202)
