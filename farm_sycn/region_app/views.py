from django.shortcuts import render

def Hello(request):
    return render(request, "landing.html")
