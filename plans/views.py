from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext

from django.views.generic.edit import CreateView,UpdateView,ProcessFormView,FormView
from django.views.generic import DetailView
from django.views.generic.base import TemplateView

from django.core.urlresolvers import reverse_lazy,reverse
# Create your views here.
from .forms import PlanForm,CreatePlanForm,PostPlanForm
from posts.models import Post
from .models import PostPlan,Plan
from .templatetags.plan_extras import get_intervals
from datetime import date,time,timedelta,datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class PostPlanFormView(FormView):
    template_name="plans/plan_create.html"
    form_class=PlanForm
    def get_queryset(self):
        post=Post.objects(slug=self.kwargs.get('slug')).first()
        return post
    def get_next_day_url(self):
        post=self.get_queryset()
        nextday=datetime.combine(date(year=int(self.kwargs.get('year')),
            month=int(self.kwargs.get('month')),
            day=int(self.kwargs.get('day'))
            )+timedelta(days=1),time(0,0))
        url=reverse('plan-create',kwargs={'slug':self.kwargs.get('slug'),
            'day':nextday.day,
            'month':nextday.month,
            'year':nextday.year
            })
        return url
    def get_back_day_url(self):
        post=self.get_queryset()
        backday=datetime.combine(date(year=int(self.kwargs.get('year')),
            month=int(self.kwargs.get('month')),
            day=int(self.kwargs.get('day'))
            )-timedelta(days=1),time(0,0))
        url=reverse('plan-create',kwargs={'slug':self.kwargs.get('slug'),
            'day':backday.day,
            'month':backday.month,
            'year':backday.year
            })
        return url        
    def form_valid(self,form):
        post=self.get_queryset()
        day=date(year=int(self.kwargs.get('year')),month=int(self.kwargs.get('month')),day=int(self.kwargs.get('month')))
        ending=form.cleaned_data['ending']
        starting=form.cleaned_data['starting']
        title=form.cleaned_data['title']
        transport=form.cleaned_data['transport']
        cost=form.cleaned_data['cost']
        content=form.cleaned_data['content']
        plan=PostPlan(date=day,ending=ending,starting=starting,title=title,transport=transport,content=content,cost=cost)
        plan.save()
        post.postplans.append(plan)
        post.save()
        return super(PostPlanFormView,self).form_valid(form)
    def get_context_data(self,*args,**kwargs):
        self.context=super(FormView,self).get_context_data(*args,**kwargs)
        context=self.context
        context['post']=self.get_queryset()
        context['intervals']=get_intervals(self.get_queryset())
        context['nextday_url']=self.get_next_day_url()
        context['backday_url']=self.get_back_day_url()
        return context
    def get_success_url(self):
        url=reverse_lazy('plan-create',kwargs={'year':self.kwargs.get('year'),
            'slug':self.kwargs.get('slug'),
            'day':self.kwargs.get('day'),
            'month':self.kwargs.get('month')
            })
        return url

class PlanCreateView(CreateView):
    form_class=PlanForm
    template_name="plans/plan_create.html"
    model=Plan

    def get_queryset(self,*args,**kwargs):
        post=Post.objects(slug=kwargs.get('slug')).first()
        today=datetime.date(year=kwargs.get('year'),month=kwargs.get('month'),day=kwargs.get('day'))
        diff=today-post.arrival.date()
        day=diff.days
        if self.object:
            self.object.day=day
            post.plans.append(self.object)
            post.save()
        return self.object

    def get_day_number(self):
        year=self.kwargs.get('year')
        month=self.kwargs.get('month')
        day=self.kwargs.get('day')
        today=datetime.date(year=int(year),month=int(month),day=int(day))
        post=Post.objects(slug=self.kwargs.get('slug')).first()
        diff=today-post.arrival.date()
        day=diff.days
        return day

    def get_context_data(self,*args,**kwargs):
        self.context=super(PlanCreateView,self).get_context_data(*args,**kwargs)
        context=self.context
        post=Post.objects(slug=self.kwargs.get('slug')).first()
        context['plans']=post.postplans
        context['post']=post
        if self.get_day_number()!=0:
            context['day_number']=self.get_day_number()+1
            context['back_day_url']=reverse('plan-create',kwargs={'slug':self.kwargs.get('slug'),'year':self.kwargs.get('year'),'month':self.kwargs.get('month'),'day':int(self.kwargs.get('day'))-1})
        elif self.get_day_number()==0:
            context['day_number']=1
        return context

    def get_success_url(self):
        year=self.kwargs.get('year')
        month=self.kwargs.get('month')
        day=self.kwargs.get('day')
        url=reverse_lazy('continue-planning',kwargs={'slug':self.kwargs.get('slug'),'year':year,'month':month,'day':day,'number':self.object.number})
        return url

class PostPlanUpdateView(UpdateView):
    model=PostPlan
    form_class=PostPlanForm
    template_name="plans/plan_update.html"

    def get_object(self):
        plan,created=PostPlan.objects.get_or_create(number=self.kwargs.get('number'))
        if created:
            pass
        return plan

    def get_queryset(self):
        if not self.instance:
            self.instance=self.get_object()
        plan=self.get_object()
        return plan

    def get_success_url(self):
        return reverse_lazy('continue-planning',kwargs={'number':self.kwargs.get('number'),'slug':self.kwargs.get('slug'),'year':self.kwargs.get('year'),'month':self.kwargs.get('month'),'day':self.kwargs.get('day')})


    '''def form_valid(self):
        starting=self.cleaned_data['starting']
        ending=self.cleaned_data['ending']
        title=self.cleaned_data['title']
        transport=self.cleaned_data['transport']
        cost=self.cleaned_data['cost']
        content=self.cleaned_data['content']'''

class PostPlanView(TemplateView):
    template_name="plans/plan_create.html"

    def get_context_data(self,*args,**kwargs):
        context=super(PostPlanView,self).get_context_data(*args,**kwargs)
        post=Post.objects.get(slug=kwargs.get('slug'))
        today=date(year=int(kwargs.get('year')),month=int(kwargs.get('month')),day=int(kwargs.get('month')))
        diff=post.arrival.date()-today
        
        userid=request.sessions['_auth_user_id']
        context['user']=User.objects.get(id=userid)
        context['post']=post
        context['form']=PostPlanForm()
        context['date']=today
        context['postplanform']=PostPlanForm()
        context['day_number']=diff.days
        return context

def postplan_update_view(request,*args,**kwargs):
    year=kwargs.get('year')
    month=kwargs.get('month')
    day=kwargs.get('day')
    slug=kwargs.get('slug')
    post=Post.objects(slug=slug).first()
    if request.method=="POST":
        form=PlanForm(request.POST)
        if form.is_valid():
            ending=form.cleaned_data['ending']
            starting=form.cleaned_data['starting']
            title=form.cleaned_data['title']
            transport=form.cleaned_data['transport']
            cost=form.cleaned_data['cost']
            content=form.cleaned_data['content']
            plan=PostPlan(title=title,transport=transport,cost=cost,content=content)
            plan.save()
            plan.starting=datetime.combine(date(year=year,month=month,day=day),starting)
            plan.ending=datetime.combine(date(year=year,month=month,day=day),ending)
            plan.save()
            post.postplans.append(plan.number)
            post.save()
            return HttpResponseRedirect(reverse('plan-create',kwargs={'slug':slug,'year':year,'month':month,'day':day}))
    else:
        plan=PostPlan.objects(number=kwargs.get('pk')).first()
        form=PlanForm()
        return render(request,'plans/plan_update.html',{'plan':plan,'form':form})

'''class DayCreateView(CreateView):
    model=DayPlan
    template_name="plans/dayplan_create.html"
    form_class=DayPlanForm

    def get_queryset(self,*args,**kwargs):
        post=Post.objects(slug=kwargs.get('slug')).first()
        dayplan=super(DayCreateView,self).get_queryset(*args,**kwargs)
        if self.instance:
            return self.instance
        else:
            return dayplan
    def get_success_url(self,*args,**kwargs):
        post=Post.objects(slug=self.kwargs.get('slug')).first()
        url=reverse_lazy('day-planning',kwargs={'slug':post.slug,'day':self.object.number })
        return url

class DayPlanning(CreateView):
    model=DayPlan
    template_name="plans/dayplan_create.html"
    form_class=DayPlanForm

    def get_queryset(self,*args,**kwargs):
        post=Post.objects(slug=kwargs.get('slug')).first()
        dayplan=DayPlan.objects(number=kwargs.get('day')).first()
        return dayplan

    def get_success_url(self,*args,**kwargs):
        url=reverse_lazy('create-plan',kwargs={'day':self.object.number,'slug':self.object.number})
        return url

    def get_context_data(self,*args,**kwargs):
        self.context=super(DayPlanning,self).get_context_data(*args,**kwargs)
        context=self.context
        context['post']=self.get_queryset()
        return context'''



def home(request):
    return render_to_response('plans/home.html',context_instance=RequestContext(request))


def create_plan(request,slug=None,num1=1):
    if slug is not None:
        post=Post.objects.get(slug=slug)
    if request.method=="POST":
        data=PlanForm(request.POST)
        if data.is_valid():
            day=data.cleaned_data['day']
            title=data.cleaned_data['title']
            transport=data.cleaned_data['transport']
            cost=data.cleaned_data['cost']
            content=data.cleaned_data['content']
            link=data.cleaned_data['link']
            picture=data.cleaned_data['picture']
            #create plan with this data
            plan=Plan(day=day,title=title,transport=transport,cost=cost,content=content,link=link,picture=picture)
            post.plans.append(plan)
            post.save()
            message=u'plan created successfully'
            return HttpResponseRedirect('/posts/')
        else:
            errors=u'some errors have been occured'
    else:
        form=PlanForm()

        return render_to_response('plans/create.html',{'post':post,'form':form},context_instance=RequestContext(request))


def plan_details(request):
    if pk is not None:
        post=Post.objects.get(id=pk)


def get_positions(arrival,departure):
    length=int(departure)-int(arrival)
    positions=[]
    left=int(arrival)*10
    width=length*10
    right=240-(departure)*10
    return positions

def plan_this_post(request,day_number,slug=None):
    if slug is not None:
        post=Post.objects.get(slug=slug)
        if request.method=="POST":
            data=PlanForm(request.POST)
            if data.is_valid():
                day=data.cleaned_data['day']
                title=data.cleaned_data['title']
                transport=data.cleaned_data['transport']
                cost=data.cleaned_data['cost']
                content=data.cleaned_data['content']
                link=data.cleaned_data['link']
                picture=data.cleaned_data['picture']
                #create plan with this data
                plan=Plan(day=day,title=title,transport=transport,cost=cost,content=content,link=link,picture=picture)
                post.plans.append(plan)
                post.save()
        else:
            form=PlanForm()
            print day_number
            if day_number:
                dayplans=DayPlan.objects(post=post).first()
                if dayplans.plans:
                    intervals=get_intervals(dayplans)
                for i,j in enumerate(dayplans.plans):
                    positions=get_positions(j.arrival,j.departure)
            return render(request,'plans/create.html',{'post':post,'form':form,'dayplans':dayplans,'intervals':intervals,'positions':positions})
    else:
        return HttpResponse("Not a valid slug")


