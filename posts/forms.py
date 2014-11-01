
from django import forms
from mongoengine.django.auth import User
from .models import Post
from django.forms.extras.widgets import SelectDateWidget

class PostForm(forms.Form):
    arrival=forms.DateField(widget=SelectDateWidget())
    departure=forms.DateField(widget=SelectDateWidget())
    title=forms.CharField(max_length=300,required=True)
    destination=forms.CharField(max_length=50)
    duration=forms.DecimalField(required=True)
    description=forms.CharField(widget=forms.Textarea)


    def __init__(self,*args,**kwargs):
        self.instance=kwargs.pop('instance',None)
        super(PostForm,self).__init__(*args,**kwargs)
        if self.instance:
            self.fields['title'].initial=self.instance.title
            self.fields['destination'].initial=self.instance.destination
            self.fields['duration'].initial=self.instance.duration
            self.fields['description'].initial=self.instance.description
            self.fields['arrival'].initial=self.instance.arrival
            self.fields['departure'].initial=self.instance.departure

    def save(self,commit=True):
        post=self.instance if self.instance else Post()
        self.arrival=self.cleaned_data['arrival']
        self.departure=self.cleaned_data['departure']
        self.title=self.cleaned_data['title']
        self.destination=self.cleaned_data['destination']
        self.duration=self.cleaned_data['duration']
        self.description=self.cleaned_data['description']

        if commit:
            post.save()

        return post
class UserRegisterForm(forms.Form):
    username=forms.CharField(max_length=30)
    password=forms.CharField(widget=forms.PasswordInput())
    email=forms.EmailField()
    first_name=forms.CharField(max_length=30)
    last_name=forms.CharField(max_length=30)

    def __init__(self,*args,**kwargs):
        self.instance=kwargs.pop('instance',None)
        super(UserRegisterForm,self).__init__(*args,**kwargs)
        if self.instance:
            self.fields['username'].initial=self.instance.username
            self.fields['password'].initial=self.instance.password
            self.fields['email'].initial=self.initial.email
            self.fields['first_name'].initial=self.instance.first_name
            self.fields['last_name'].initial=self.instance.last_name
    def save(self,commit=True):
        user=self.instance if self.instance else User()
        self.username=self.cleaned_data['username']
        self.password=self.cleaned_data['password']
        self.email=self.cleaned_data['email']
        self.first_name=self.cleaned_data['first_name']
        self.last_name=self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username=forms.CharField(max_length=30)
    password=forms.CharField(widget=forms.PasswordInput())