from django.forms import ModelForm
from django import forms
from .models import Geolocation
from .models import Cooperative
from .models import User
from .models import Stock_management
from .models import System
from .models import Notification
from .models import Fail_type
from .models import System



class UserForm(ModelForm):
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
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CooperativeForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['user'].initial = user
            self.fields['user'].widget.attrs['readonly'] = True

# forms.py
from django import forms
from .models import Stock_management, System

class StockManagementForms(forms.ModelForm):
    quality = forms.ModelChoiceField(queryset=System.objects.all(), required=True, label="Select quality")
    
    class Meta:
        model = Stock_management
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        cooperative = kwargs.pop('cooperative', None) 
        super().__init__(*args, **kwargs)  
        
        if cooperative:
            self.fields['cooperative'].initial = cooperative
            self.fields['cooperative'].widget.attrs['readonly'] = True

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
