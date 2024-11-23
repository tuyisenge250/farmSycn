from django.shortcuts import render

def Hello(request):
    return render(request, "landing.html")

def dashboard(request):
    return render(request, 'dashboard.html')

def home(request):
    return render(request, 'home.html')

def signup(request):
    return render(request, 'signup.html')

def overview(request):
    return render(request, 'overview.html')

def notification(request):
    return render(request, 'notification.html')

def complete_account(request):
    return render(request, 'complete_account.html')

def stock_mngt(request):
    return render(request, 'stock_mngt.html')

def login(request):
    return render(request, 'login.html')

def add_mngt(request):
    return render(request,"add_mngt.html")
