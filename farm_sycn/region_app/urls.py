from django.urls import path
from . import views

urlpatterns = [
               path('', views.Hello, name="landing"), 
               path('home/', views.home, name="Home"),
               path('home/<int:id>', views.overview, name="overviews"),
               path('login/', views.login, name="login"),
               path('sinup/', views.signup, name='sinup'),
               path('dashboard/', views.dashboard, name="dashboard"),
               path('sinup/coopinfo', views.complete_account, name="complete_acc"),
               path('notification/', views.notification, name="notification"),
               path('stockManagement/', views.stock_mngt, name="management"),
               path('scockManagement/add', views.add_mngt, name="add")
               ]
