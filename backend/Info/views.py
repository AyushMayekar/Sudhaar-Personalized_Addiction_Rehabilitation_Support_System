from django.shortcuts import render

def addictions(request):
    return render(request, 'Addictions.html')

def Aboutus(request):
    return render(request, 'Aboutus.html')