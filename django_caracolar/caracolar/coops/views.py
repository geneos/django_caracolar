from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
def JsonView(request):
    responseData = {
        'clave1': 'Test Response 1',
        'clave2': 'Test Response 2',
        'clave3' : 'Test Response 3'
    }

    return JsonResponse(responseData)
