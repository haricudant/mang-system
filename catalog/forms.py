from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime
from django import forms
from .models import Employee, Book
import boto3

from django.contrib.auth import(authenticate, get_user_model)


User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=  forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password =  self.cleaned_data.get('password')



        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user does not exists')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect Password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
        return  super (UserLoginForm, self).clean(*args,**kwargs)




class UserRegisterForm(forms.ModelForm):
    email =forms.EmailField(label='Email address')
    email2 = forms.EmailField (label= 'Confirm Email')
    password = forms.CharField(widget=forms.PasswordInput)


    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password'
        ]


        def clean (self, *args, **kwargs):
            email = self.cleaned_data.get('email')
            email2 = self.cleaned_data.get('email2')
            if email != email:
                raise forms.ValidationError('Emails must match')
            email_qs=User.objects.filter(email = email)

            if email_qs.exists():
                raise forms.validatioError("This email has already been registered")
            return super(UserRegisterForm, self).clean(*args,**kwargs)




# class RenewBookForm(forms.Form):
#     """
#     Form for a librarian to renew books.
#     """
#     renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")
#
#     def clean_renewal_date(self):
#         data = self.cleaned_data['renewal_date']
#
#         #Check date is not in past.
#         if data < datetime.date.today():
#             raise ValidationError(_('Invalid date - renewal in past'))
#         #Check date is in range librarian allowed to change (+4 weeks)
#         if data > datetime.date.today() + datetime.timedelta(weeks=4):
#             raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
#
#         # Remember to always return the cleaned data.
#         return data
#
#
# FRUIT_CHOICES= [
#     ('orange', 'Oranges'),
#     ('cantaloupe', 'Cantaloupes'),
#     ('mango', 'Mangoes'),
#     ('honeydew', 'Honeydews'),
#     ]



class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"