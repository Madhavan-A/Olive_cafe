from django.shortcuts import render

def home(request):
    return render(request, 'home/index.html')

def booking(request):
    return render(request, 'home/booking.html')