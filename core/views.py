# core/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests

def index(request):
    ip = get_client_ip(request)
    location = get_location(ip)
    return render(request, 'index.html', {'ip': ip, 'location': location})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')

def get_location(ip):
    try:
        response = requests.get(f'https://ipapi.co/{ip}/json/')
        data = response.json()
        return f"{data.get('city', 'Unknown')}, {data.get('country_name', 'Unknown')}"
    except:
        return "Unknown"

@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})