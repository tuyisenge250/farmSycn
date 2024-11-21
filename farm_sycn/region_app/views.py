from django.shortcuts import render,HttpResponse

def Hello(request):
    return HttpResponse("Hello Django sycn Farmer")
