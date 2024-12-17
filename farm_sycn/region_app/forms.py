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
        exclude = ['status', 'number_managers']
    labels = {
        'full_name' : 'cooperative Name full Name',
        'abv_name' : 'Abbreviation Name',
        'email' : "cooperative Email"
    }
    widgets = {
        'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'cooperative Name full Name'})
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

class GeolocationForm(ModelForm):
    class Meta:
        model = Geolocation
        fields = "__all__"

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['email', 'comment']

class MessageResponseForm(ModelForm):
    class Meta:
        model = Message
        fields = ['reply']

class SystemForm(ModelForm):
    class Meta:
        model = System
        exclude = ['cooperative']
    
class LoginForm(forms.Form):
    userName = forms.CharField(max_length= 100)
    password = forms.CharField(widget=forms.PasswordInput)

class SystemResolutionForm(forms.ModelForm):
    class Meta:
        model = System
        fields = ['resolution_steps', 'resolved']
        widgets = {
            'resolution_steps': forms.Textarea(attrs={'rows': 4}),
            'resolved': forms.CheckboxInput(),
        }
