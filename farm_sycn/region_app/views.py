from django.shortcuts import render, get_object_or_404, get_list_or_404,redirect
from django.urls import reverse
from .models import Geolocation
from .models import Cooperative
from .models import User
from .models import Stock_management
from .models import System
from .models import Notification
from .models import Fail_type
from .forms import UserForm, CooperativeForm, StockManagementForm, QualityForm, FailTypeForm, MessageForm

def Hello(request):
    return render(request, "landing.html")

def dashboard(request, id):
    system = get_list_or_404(System, cooperative_id=id)
    mngt = get_list_or_404(Stock_management, cooperative_id=2)
    cooperative = get_object_or_404(Cooperative, pk=id)
    dash_info = {
        "name": cooperative.user.full_name,
        "coop_info": cooperative,
        "system_info": system[:5],
        "management":  mngt[:5],
    }
    return render(request, 'dashboard.html', {"dashboard": dash_info})

def home(request):
    if request.method == "POST":
        message = MessageForm(request.POST)
        message.save()
    geolocation = Geolocation.objects.all()
    return render(request, 'home.html', {'locationCoop': geolocation})

def signup(request):
    if request.method == 'POST':
        forms = UserForm(request.POST)
        if forms.is_valid():
            user = forms.save()
            print(user.id) 
            return redirect(reverse('complete_account', kwargs={'id': user.id}))

        else:
            return render(request, 'signup.html', {'form': forms})
    else:
        context = {}
        context['form'] = UserForm()
        return render(request, 'signup.html', context)

def overview(request, id):
    coop = get_object_or_404(Cooperative,pk=id)
    return render(request, 'overview.html', {'cooperative_info': coop})

def notification(request, id):
    notification = get_list_or_404(Notification, cooperative_id=id)
    return render(request, 'notification.html', {"nots": notification})

def complete_account(request, id):
    user  = User.objects.get(pk=id)
    if request.method == "POST":
        forms = CooperativeForm(request.POST, request.FILES)
        print(forms)
        if forms.is_valid():
            cooperative = forms.save(commit=False)
            cooperative.user = user
            cooperative.save()
            return redirect('login')
        else:
            return render(request, 'complete_account.html', {'form': forms})
    else:
        forms = CooperativeForm()
    return render(request, 'complete_account.html', {'form': forms})

def stock_mngt(request, id):
    stock = get_list_or_404(Stock_management, cooperative_id=id)
    return render(request, 'stock_mngt.html', {'stocks': stock})

def login(request):
    return render(request, 'login.html')

def add_mngt(request, id):
    cooperative = get_object_or_404(Cooperative, pk=id)
    
    if request.method == "POST":
        form = StockManagementForm(request.POST)
        
        if form.is_valid():
            # Extract form data
            flow_type = form.cleaned_data['flows_ch']  # 'IN' or 'OUT'
            quantity = form.cleaned_data['quantity']
            quality = form.cleaned_data['quality']
            
            # Get existing stocks for this cooperative and quality
            exist_stocks = Stock_management.objects.filter(cooperative=cooperative, quality=quality).order_by('-id')
            
            # Calculate remaining quantity
            remainQ = exist_stocks[0].total_quantity_quality if exist_stocks.exists() else 0
            
            if flow_type == "IN":
                remainQ += quantity
            else:
                if(remainQ > quantity):
                    remainQ -= quantity
                else:
                    raise ValueError("your quantity not remain")            
            stock_record = form.save(commit=False)
            stock_record.cooperative = cooperative
            stock_record.total_quantity_quality = remainQ
            stock_record.save()
            
            return redirect(reverse('management', kwargs={'id': id}))
        else:
            print(form.errors) 
    
    else:
        form = StockManagementForm()
    
    return render(request, "add_mngt.html", {'form': form})

