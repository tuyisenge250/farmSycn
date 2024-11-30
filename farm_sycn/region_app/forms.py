from django.forms import ModelForm
from django import forms
from .models import Geolocation
from .models import Cooperative
from .models import User
from .models import Stock_management
from .models import System
from .models import Quality
from .models import Notification
from .models import Fail_type
from .models import System, Message


class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = "__all__"
    labels = {
        'full_name' : 'your cooperative Name full Name',
        'abv_name' : 'Abbreviation Name',
        'email' : "cooperative Email"
    }

class CooperativeForm(ModelForm):
    class Meta:
        model = Cooperative
        exclude = ['user']


class StockManagementForm(forms.ModelForm):
    quality = forms.ModelChoiceField(queryset=Quality.objects.all(), required=True, label="Select quality")
    class Meta:
        model = Stock_management
        exclude = ['cooperative', 'total_quantity_quality']

class FailTypeForm(ModelForm):
    class Meta:
        model = Fail_type
        fields = "__all__"

class QualityForm(ModelForm):
    class Meta:
        model = System
        fields = "__all__"

# class GeolocationForm(ModelForm):
#     class Meta:
#         model = Geolocation
#         fields = "__all__"

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['email', 'comment']