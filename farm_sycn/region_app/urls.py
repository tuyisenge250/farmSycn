from django.urls import path
from . import views

urlpatterns = [
               path('', views.Hello, name="landing"), 
               path('home/', views.home, name="Home"),
               path('home/<int:id>', views.overview, name="overviews"),
               path('login/', views.login, name="login"),
               path('signup/', views.signup, name='signup'),
               path('dashboard/<int:id>', views.dashboard, name="dashboard"),
               path('complete_account/<int:id>', views.complete_account, name='complete_account'),
               path('notification/<int:id>', views.notification, name="notification"),
               path('management/<int:id>', views.stock_mngt, name="management"),
               path('management/<int:id>/add/', views.add_mngt, name="add"),
               path('system/<int:id>', views.system, name="system"),
               path('admindashboard/<int:id>', views.adminDashboard, name="Admin"),
               path('dashboard/system/<int:id>', views.system_dashboard, name="dashboard_system"),
               path('adminusers/<int:id>', views.adminUsers, name="adminuser"),
               path('adminchange/<int:id>', views.admin_changes, name='changes'),
               path('adminnotification/<int:id>', views.admin_notification, name='admin_notification'),
               path('adminfeedback/', views.admin_messages, name="feedbacks"),
               path('dashboard/profile/<int:id>', views.profile, name="profile"),
               path('system/<int:id>/resolve/', views.resolve_system_issue, name='resolve_system_issue'),
               path('adminissues/<int:id>', views.admin_issues, name='issues'),
               ]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

