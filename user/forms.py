from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

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


class Create_group_form(forms.ModelForm):
    permission=forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="select Your choice"
    )
    
    class Meta:
        model=Group
        fields=["name","permission"]

class Assign_role_form(forms.Form):
    role=forms.ModelChoiceField(
        queryset=Group.objects.all(),
        label="Assign a Group"
    )

