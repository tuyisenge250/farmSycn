from django.shortcuts import render, get_object_or_404, get_list_or_404,redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import make_password
from django.urls import reverse
import json
from .models import Geolocation
from .models import Cooperative
from .models import User
from .models import Stock_management
from .models import System
from .models import Notification,Message
from .models import Fail_type
from .forms import UserForm, CooperativeForm, StockManagementForm, QualityForm, FailTypeForm, MessageForm, GeolocationForm, SystemForm, LoginForm, SystemResolutionForm, MessageResponseForm
from django.utils.timezone import now
from .utils import get_coordinates
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.dateformat import format

def Hello(request):
    return render(request, "landing.html")

def dashboard(request, id):
    system = System.objects.filter(cooperative_id=id)
    cooperative = get_object_or_404(Cooperative, pk=id)
    noti = Notification.objects.filter(system_id=id).count() if Notification.objects.filter(system_id=id).exists() else 0
    metrics = matrics(id)

    serialized_system = json.dumps(
        [{"temperature_change": s.temperature_change, "last_update": s.last_update.strftime('%Y-%m-%d %H:%M:%S')} for s in system],
        cls=DjangoJSONEncoder)


    context = {
        "id": cooperative.id,
        "name": cooperative.user.full_name,
        'metrics': metrics,
        "coop_info": cooperative,
        "system_info": system[:5],
        'system': serialized_system,  # Pass serialized data
        'notiValue': noti,
    }
    return render(request, 'dashboard.html', context)

def home(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = MessageForm()
    geolocation = Geolocation.objects.all()
    return render(request, 'home.html', {'locationCoop': geolocation, 'form': form})

def matrics(id):
    mngt = Stock_management.objects.filter(cooperative_id=id)    
    green = [[item.total_quantity_quality,item.expired_date] for item in mngt if item.quality.name == 'Green(unripe)']
    ripe = [[item.total_quantity_quality, item.expired_date] for item in mngt if item.quality.name == 'Ripe(Fresh)']
    cherry = [[item.total_quantity_quality, item.expired_date] for item in mngt if item.quality.name == 'Cherry']
    processing = [[item.total_quantity_quality, item.expired_date] for item in mngt if item.quality.name == 'Processing']
    metrics = [
    {
        "name": "Cherry",
        "icon_class": "fa-solid fa-seedling",
        "data": cherry[-1] if cherry else 0,
        "color": "green",
    },
    {
        "name": "Ripe Fresh",
        "icon_class": "fa-solid fa-circle-check",
        "data": ripe[-1] if ripe else 0,
        "color": "yellow",
    },
    {
        "name": "Green (Unripe)",
        "icon_class": "fa-solid fa-seedling green",
        "data": green[-1] if green else 0,
        "color": "green",
    },
    {
        "name": "Processing",
        "icon_class": "fa-solid fa-spinner fa-spin processing",
        "data": processing[-1] if processing else 0,
        "color": "blue",
    },
    ]
    return metrics

def signup(request):
    if request.method == 'POST':
        forms = UserForm(request.POST)
        if forms.is_valid():
            user = forms.save(commit=False)
            user.status = 'unproved'
            user.number_managers = 3
            user.save()
            print(user.id) 
            print(user.role)
            if user.role == "AD":
                return redirect('login')
            return redirect(reverse('complete_account', kwargs={'id': user.id}))

        else:
            context={
                'error': "Use name already used or login",
                'form': forms
            }
            return render(request, 'signup.html', context)
    else:
        context = {}
        context['form'] = UserForm()
        return render(request, 'signup.html', context)

def profile(request, id):
    cooperative = get_object_or_404(Cooperative, pk=id)
    stock = Stock_management.objects.filter(cooperative_id=id)
    noti = Notification.objects.filter(system_id=id).count() if Notification.objects.filter(system_id=id).exists() else 0
    coop = get_object_or_404(Cooperative,pk=id)
    metrics = matrics(id)
    context = {
        'id' :  coop.id,
        'metrics': metrics,
        'stocks': stock,
        'notiValue': noti,
        'cooperative_info': coop,
    }
    return render(request, 'profile.html', context)

def overview(request, id):
    coop = get_object_or_404(Cooperative,pk=id)
    matric = matrics(id)
    context = {
        'cooperative_info': coop,
        'metrics': matric,
        }
    return render(request, 'overview.html', context)

def notification(request, id, active_message_id=None):
    notifications = Notification.objects.filter(system_id=id)
    cooperative = get_object_or_404(Cooperative, pk=id)
    stock = Stock_management.objects.filter(cooperative_id=id)
    noti = Notification.objects.filter(system_id=id).count() if Notification.objects.filter(system_id=id).exists() else 0
    metrics = matrics(id)
    
    for notification in notifications:
        notification.truncated_message = notification.message[:37]
        notification.name = notification.system.user.full_name
    
    active_notification = (
        get_object_or_404(Notification, pk=active_message_id) 
        if active_message_id else notifications[0]
    )
    
    context = {
        'id': cooperative.id,
        'metrics': metrics,
        'stocks': stock,
        'notifications': notifications,
        'active_notification': active_notification,
        'notiValue': noti,
    }
    return render(request, 'notification.html', context)

def complete_account(request, id):
    user = User.objects.get(pk=id)
    if request.method == "POST":
        forms = CooperativeForm(request.POST, request.FILES)
        if forms.is_valid():
            cooperative = forms.save(commit=False)
            cooperative.user = user
            cooperative.save()

            village = ""
            cell = ""
            sector = cooperative.location_sector
            district = cooperative.location_district
            province = cooperative.location_province
            location = get_coordinates(village, cell, sector, district, province)
            print(location)
            if location:
                geolocation = Geolocation()
                geolocation.cooperative = cooperative
                geolocation.latitude = location.get('latitude', None)
                geolocation.longitude = location.get('longitude', None)
                geolocation.address = f"{village}, {cell}, {sector}, {district}, {province}, Rwanda"
                geolocation.save()
            else:
                return render(request, 'complete_account.html', {'form': forms, 'error': 'Invalid location information.'})

            return redirect('login') 
        else:
            print(forms.errors)
            context = {
                'error': "There was a problem with your form submission. Please check the errors.",
                'form': forms
            }
            return render(request, 'complete_account.html', context)
    else:
        forms = CooperativeForm()

    return render(request, 'complete_account.html', {'form': forms})

def stock_mngt(request, id):
    cooperative = get_object_or_404(Cooperative, pk=id)
    stock = Stock_management.objects.filter(cooperative_id=id)
    noti = Notification.objects.filter(system_id=id).count() if Notification.objects.filter(system_id=id).exists() else 0
    last_system_commit = System.objects.filter(cooperative_id=id).order_by('-id').first()
    metrics = matrics(id)
    context = {
        'id' :  cooperative.id,
        'metrics': metrics,
        'stocks': stock,
        'notiValue': noti,
        'system': last_system_commit,
    }
    return render(request, 'stock_mngt.html', context)

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['userName']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(full_name=full_name)
                if user.status == 'uproved':
                    context = {
                        'form': form,
                        'error': "You have to await admin approval."
                    }
                    return render(request, 'login.html', context)
                if user.password == password and user.status == 'proved':
                    if user.role == 'manager':
                        request.session['user_id'] = user.id
                        return redirect(reverse('dashboard', kwargs={'id': user.id})) 
                    else:
                        request.session['user_id'] = user.id
                        return redirect(reverse('Admin', kwargs={'id': user.id})) 
                else:
                    context = {
                        'form': form,
                        'error': "Incorrect password or full name."
                    }
                    return render(request, 'login.html', context)
            except User.DoesNotExist:
                context = {
                    'form': form,
                    'error': "Invalid full name or password."
                }
                return render(request, 'login.html', context)
    else:
        form = LoginForm()
        context = {
            'form': form
        }
    return render(request, 'login.html', context)

def add_mngt(request, id):
    cooperative = get_object_or_404(Cooperative, pk=id)
    
    if request.method == "POST":
        form = StockManagementForm(request.POST)
        
        if form.is_valid():
            flow_type = form.cleaned_data['flows_ch']
            quantity = form.cleaned_data['quantity']
            quality = form.cleaned_data['quality']
            exist_stocks = Stock_management.objects.filter(cooperative=cooperative, quality=quality).order_by('-id')
            
            remainQ = exist_stocks[0].total_quantity_quality if exist_stocks.exists() else 0
            
            if flow_type == "IN":
                remainQ += quantity
            else:
                if(remainQ > quantity):
                    remainQ -= quantity
                else:
                    error = "your quantity not remain"
                    form = StockManagementForm()
                    context = {
                        'error' : error,
                        'form' : form,
                        }
                    return render(request, "add_mngt.html", context)            
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

def system(request, id):
    cooperative = get_object_or_404(Cooperative, pk=id)
    last_system_commit = System.objects.filter(cooperative=cooperative).order_by('-id').first()
    
    if request.method == 'POST':
        form = SystemForm(request.POST)
        if form.is_valid():
            system = form.save(commit=False)
            system.cooperative = cooperative
            system.failed = False 
            
            temp = system.temperature_change
            hum = system.humidity_change
            if last_system_commit and (
                abs(last_system_commit.temperature_change - temp) > 5 or
                abs(last_system_commit.humidity_change - hum) > 10
            ):
                system.failed = True
            
            system.save()
            
            notification = Notification(
                system=system.cooperative,
                message=(
                    f"System Failure Alert: Temperature: {temp}, "
                    f"Humidity: {hum}, Status: {'Fail' if system.failed else 'Normal'}"
                ),
                status="fail" if system.failed else "normal"
            )
            notification.save()

            return redirect(reverse('admin_notification', kwargs={"id": 1}))
    else:
        form = SystemForm()
    return render(request, 'system.html', {'form': form})

def adminDashboard(request, id=1):
    unproved_users_count = User.objects.filter(status='unproved').count()
    cooperative_list = Cooperative.objects.all()
    recent_systems = System.objects.all().order_by('-last_update')[:5]
    count_system = System.objects.filter(Q(status='normal') | Q(resolved=True)).count()
    system = System.objects.all()
    total_system = System.objects.all().count()
    error_system = total_system - count_system
    serialized_system = json.dumps(
        [{"temperature_change": s.temperature_change, "last_update": s.last_update.strftime('%Y-%m-%d %H:%M:%S')} for s in system],
        cls=DjangoJSONEncoder)

    context = {
        'user_count': unproved_users_count,
        'cooperatives': cooperative_list,
        'recent_systems': recent_systems,
        'system': count_system,
        'system_info': serialized_system,
        'system_error': error_system,
    }
    print(error_system)
    return render(request, 'AdminDashboard.html', context)

def adminUsers(request, id=1):
    unproved_users_count = User.objects.filter(status='unproved').count()
    cooperative_list = Cooperative.objects.all()
    count_system = System.objects.filter(status='active').count()
    users = User.objects.all()
    total_system = System.objects.all().count()
    error_system = total_system - count_system
    form = None 

    if request.method == 'POST':
        if 'prove' in request.POST:  # Handle Prove/Unprove
            pk = request.POST.get('prove')
            user = get_object_or_404(User, id=pk)
            user.status = 'proved' if user.status == 'unproved' else 'unproved'
            user.save()

        elif 'delete' in request.POST:  # Handle Delete
            pk = request.POST.get('delete')
            user = get_object_or_404(User, id=pk)
            user.delete()

        elif 'edit' in request.POST:  # Open Edit Form
            pk = request.POST.get('edit')
            user = get_object_or_404(User, id=pk)
            form = UserForm(instance=user)

        elif 'save' in request.POST:  # Save Edited Data
            pk = request.POST.get('save')  # Hidden input to identify user ID
            user = get_object_or_404(User, id=pk)
            form = UserForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('adminuser', id=2)  # Redirect to avoid resubmission

    context = {
        'user_count': unproved_users_count,
        'cooperatives': cooperative_list,
        'system': count_system,
        'users': users,
        'system_error': error_system,
        'form': form,  # Pass the form to the template
    }
    return render(request, 'adminusers.html', context)

def system_dashboard(request, id):
    cooperative = get_object_or_404(Cooperative, pk=id)
    system = get_list_or_404(System, cooperative_id=id)
    noti = Notification.objects.filter(system_id=id).count() if Notification.objects.filter(system_id=id).exists() else 0
    count_system = System.objects.filter(status='active').count()
    total_system = System.objects.all().count()
    error_system = total_system - count_system
    metrics = matrics(id)
    context = {
        "id" : cooperative.id,
        'metrics': metrics,
        'system': system,
        'system_error': error_system,
        'notiValue': noti
    }
    return render(request, 'dashboard_system.html', context )

def admin_changes(request, id):
    unproved_users_count = User.objects.filter(status='unproved').count()
    cooperative_list = Cooperative.objects.all()
    count_system = System.objects.filter(status='active').count()
    system  = System.objects.all()
    total_system = System.objects.all().count()
    error_system = total_system - count_system
    context = {
        'user_count': unproved_users_count,
        'cooperatives': cooperative_list,
        'system': count_system,
        'system_error': error_system,
        'all_systems_change': system,
    }
    return render(request, 'adminchanges.html', context)

def admin_notification(request, id=1):
    unproved_users_count = User.objects.filter(status='unproved').count()
    cooperative_list = Cooperative.objects.all()
    count_system = System.objects.filter(status='active').count()
    notifications = Notification.objects.all()
    total_system = System.objects.all().count()
    error_system = total_system - count_system
    for notification in notifications:
        notification.truncated_message = notification.message[:60]
    context = {
        'user_count': unproved_users_count,
        'cooperatives': cooperative_list,
        'system': count_system,
        'notification': notifications
    }
    return render(request, 'admin_notification.html', context)

def admin_messages(request):
    unproved_users_count = User.objects.filter(status='unproved').count()
    cooperative_list = Cooperative.objects.all()
    count_system = System.objects.filter(status='active').count()
    users = User.objects.all()
    messages = Message.objects.all()
    total_system = System.objects.all().count()
    error_system = total_system - count_system
    for message in messages:
        message.short_title = message.comment[:20]
    
    if request.method == 'POST':
        form = MessageResponseForm(request.POST)
        if form.is_valid():
            message_id = request.POST.get('message_id')  
            message = get_object_or_404(Message, id=message_id)
            
            message.reply = form.cleaned_data['reply']
            message.save()
            
            subject = f"Reply to your message for Farm sycn"
            message_body = f"Dear User,\n\nWe have responded to your message titled '{message.comment}'.\n\nReply:\n{form.cleaned_data['reply']}\n\nBest regards,\nAdmin Team"
            recipient_email = message.email  
            sender_email = "benjaminwell250@gmail.com" 
            
            try:
                send_mail(
                    subject,
                    message_body,
                    sender_email,
                    [recipient_email],
                    fail_silently=False,  
                )
            except Exception as e:
                print(f"Error sending email: {e}") 
            
            return redirect('feedbacks')  
    
    else:
        form = MessageResponseForm()

    context = {
        'user_count': unproved_users_count,
        'cooperatives': cooperative_list,
        'system': count_system,
        'users': users,
        'messages': messages,
        'system_error': error_system,
        'form': form
    }
    return render(request, 'admin_feedback.html', context)

def admin_issues(request, id=1):
    unproved_users_count = User.objects.filter(status='unproved').count()
    cooperative_list = Cooperative.objects.all()
    count_system = System.objects.filter(status='normal').count()
    issues_system = System.objects.filter(failed=True)
    total_system = System.objects.all().count()
    error_system = total_system - count_system
    issues_system_sorted = sorted(issues_system, key=lambda x: x.last_update, reverse=True)

    seen_cooperatives = set()
    issues = []
    for issue in issues_system_sorted:
        if issue.cooperative.id not in seen_cooperatives:
            issues.append(issue)
            seen_cooperatives.add(issue.cooperative.id)
    
    solved = []
    seen_cooperatives_solved = set()
    for solve in issues_system_sorted:
        if solve.resolved and solve.cooperative.id not in seen_cooperatives_solved:
            solved.append(solve)
            seen_cooperatives_solved.add(solve.cooperative.id)
    
    context = {
        'user_count': unproved_users_count,
        'cooperatives': cooperative_list,
        'system': count_system,
        'issues': issues,
        'system_error': error_system,
        'solved': solved,
    }
    return render(request, 'admin_issues.html', context)

def resolve_system_issue(request, id):
    system = get_object_or_404(System, pk=id)
    
    if request.method == 'POST':
        form = SystemResolutionForm(request.POST, instance=system)
        if form.is_valid():
            system = form.save(commit=False)
            system.resolved_by = request.user.full_name if request.user.is_authenticated else "Admin"
            system.resolved_at = now()
            system.save()
            
            Notification.objects.create(
                system=system,
                message=f"Issue resolved: {system.resolution_steps}",
                status="resolved"
            )
            
            return redirect('system_detail', id=system.id)
    else:
        form = SystemResolutionForm(instance=system)

    return render(request, 'resolve_system.html', {'form': form, 'system': system})
