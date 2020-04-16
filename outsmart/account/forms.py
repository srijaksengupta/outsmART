from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

def validate_mcgill_email(value):
    if not value.endswith('mcgill.ca'):
        raise ValidationError(
            'Email not from mcgill domain',
            code = 'not_mcgill'
        )

class SignupForm(forms.Form):
    username = forms.CharField( 
      # error_messages={'required': 'Gotta make a username!'}
    )
    
    email = forms.EmailField(
      validators=[validate_mcgill_email], 
      error_messages={'not_mcgill': 'mcgill members only'})
    
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField()

    
    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        
        # Validation involving multiple fields
        if 'password' in cleaned_data and 'password_confirm' in cleaned_data and cleaned_data['password'] != cleaned_data['password_confirm']:
            self.add_error('password_confirm', 'Passwords do not match')
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Login failed')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
        return super(LoginForm, self).clean(*args, **kwargs)
