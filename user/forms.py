from django import forms
from django.contrib.auth import get_user_model

User=get_user_model()


class RegistrationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    confirmpassword=forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=["username","email","password"]

    def clean_email(self):
        email=self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already exists")
        

        return email
    
    def clean(self):
        clean_data=super().clean()
        p1=clean_data.get('password')
        p2=clean_data.get('confirmpassword')

        if p1 and p2 :
            if p1!=p2:
                raise forms.ValidationError("the password aew not same")
            
        return clean_data
    

class login_form(forms.Form):
    username=forms.CharField(max_length=100)
    password=forms.CharField(widget=forms.PasswordInput)
    

