from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from home.models import applicationUser
from home.fields import ListTextWidget

class UserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class applicationUserForm(forms.ModelForm):
    class Meta:
        model = applicationUser
        fields = ['IFB_member', 'country', 'location', 'position']

    def __init__(self, *args, **kwargs):
        _country_list = kwargs.pop('data_list', None)
        super(applicationUserForm, self).__init__(*args, **kwargs)
        self.fields['country'].widget = ListTextWidget(data_list=_country_list,  name='country-list')
        for visible in self.visible_fields():
            if visible.field.widget.input_type != 'checkbox':
                visible.field.widget.attrs['class'] = 'form-control'



class contactForm(forms.Form):

    firstName = forms.CharField(label='First name', max_length=100, required=True)
    lastName = forms.CharField(label='Last name', max_length=100, required=True)
    email = forms.EmailField(label='Last name', max_length=100, required=True)
    subject = forms.CharField(label='Subject', max_length=100, required=True)
    message = forms.CharField(widget=forms.Textarea)
    cc_myself = forms.BooleanField(required=False, label="Add your mail in cc",
                                   help_text="Check to add your email in cc")

    def __init__(self, *args, **kwargs):

        super(contactForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if hasattr(visible.field.widget, 'input_type'):
                if visible.field.widget.input_type != 'checkbox':
                    visible.field.widget.attrs['class'] = 'form-control'
            else:
                visible.field.widget.attrs['class'] = 'form-control'