from django import forms

from django.forms.extras.widgets import SelectDateWidget
from datetime import datetime,time,timedelta,date
from .models import Plan,PostPlan

class PlanForm(forms.Form):
    starting_time=forms.TimeField()
    ending_time=forms.TimeField()
    title=forms.CharField(max_length=200,required=True)
    transport=forms.CharField(max_length=200)
    cost=forms.DecimalField(required=True)
    content=forms.CharField(widget=forms.Textarea)

    def __init__(self,*args,**kwargs):
        self.instance=kwargs.pop('instance',None)
        super(PlanForm,self).__init__(*args,**kwargs)
        if self.instance:
            self.fields['starting'].initial=self.instance.starting
            self.fields['ending'].initial=self.instance.ending
            self.fields['title'].initial=self.instance.title
            self.fields['transport'].initial=self.instance.transport
            self.fields['cost'].initial=self.instance.cost
            self.fields['content'].initial=self.instance.content
    
    def save(self,commit=True):
        plan=self.instance if self.instance else PostPlan()
        starting=self.cleaned_data['starting']
        ending=self.cleaned_data['ending']
        self.starting=starting.hour*60+starting.minute
        self.ending=ending.hour*60+ending.minute
        self.title=self.cleaned_data['title']
        self.transport=self.cleaned_data['transport']
        self.cost=self.cleaned_data['cost']
        self.content=self.cleaned_data['content']

        if commit:
            plan.save()
        return plan

class CreatePlanForm(forms.Form):
    starting=forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    ending=forms.TimeField(widget=forms.TimeInput(format='%H:%M'))

    def __init__(self,*args,**kwargs):
        self.instance=kwargs.pop('instance',None)
        super(CreatePlanForm,self).__init__(*args,**kwargs)
        if self.instance:
            self.fields['starting'].initial=self.instance.starting
            self.fields['ending'].initial=self.instance.ending
    def save(self,commit=True):
        plan=self.instance if self.instance else Plan()
        self.starting=self.cleaned_data['starting']
        self.ending=self.cleaned_data['ending']
        return plan

class PostPlanForm(forms.Form):
    starting=forms.DecimalField(widget=forms.TimeInput(format='%H:%M'))
    ending=forms.DecimalField(widget=forms.TimeInput(format='%H:%M'))
    def __init__(self,*args,**kwargs):
        self.instance=kwargs.pop('instance',None)
        super(PostPlanForm,self).__init__(*args,**kwargs)
        if self.instance:
            self.fields['starting'].initial=self.instance.starting
            self.fields['ending'].initial=self.instance.ending

    def save(self,commit=True,*args,**kwargs):
        plan=self.instance if self.instance else PostPlan()
        self.starting=self.cleaned_data['starting']
        self.ending=self.cleaned_data['ending']
        if commit:
            plan.save()
        return plan
