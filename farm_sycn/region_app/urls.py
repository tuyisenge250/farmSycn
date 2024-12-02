from django.urls import path
from . import views

urlpatterns = [
               path('', views.Hello, name="landing"), 
               path('home/', views.home, name="Home"),
               path('home/<int:id>', views.overview, name="overviews"),
               path('login/', views.login, name="login"),
               path('signup/', views.signup, name='signup'),
               path('dashboard/<int:id>', views.dashboard, name="dashboard"),

               path('singup/coopinfo', views.complete_account, name="complete_acc"),

               path('complete_account/<int:id>', views.complete_account, name='complete_account'),

               path('notification/<int:id>', views.notification, name="notification"),
               path('management/<int:id>', views.stock_mngt, name="management"),
               path('management/<int:id>/add/', views.add_mngt, name="add"),
               ]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

