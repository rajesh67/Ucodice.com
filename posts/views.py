from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseForbidden
from django.template import RequestContext
from mongoengine.django.auth import User

from django.contrib.auth import authenticate,login,logout
# Create your views here.
from .forms import PostForm,UserRegisterForm,LoginForm
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm

from django.views.generic.edit import CreateView,DeleteView,UpdateView,FormMixin
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View,FormView
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse_lazy,reverse


from mongoengine.queryset import DoesNotExist
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import *

#class-based views
class PostListView(ListView):
    model=Post
    template_name='posts/post_list.html'


    def get_queryset(self,**kwargs):
        return Post.objects

    def get_context_data(self, **kwargs):
        self.context = super(PostListView, self).get_context_data(**kwargs)
        self.context['post_page_url'] = reverse_lazy('post-details',kwargs={'slug':kwargs.get('slug')})
        return self.context
def post_details(request,slug=None):
    if slug:
        post=Post.objects(slug=slug).first()
        year=post.arrival.year
        month=post.arrival.month
        day=post.arrival.day
    return render(request,'posts/post_detail.html',{'post':post,'year':year,'month':month,'day':day})

class PostCreateView(CreateView):
    form_class=PostForm
    model=Post
    template_name="posts/post_create.html"

class PostUpdateView(FormView):
    form_class=PostForm
    initial={}
    template_name="posts/post_update.html"
    def get_success_url(self):
        post=self.get_queryset()
        url=reverse_lazy('post-details',kwargs={'slug':post.slug})
        return url
    def get_queryset(self,*args,**kwargs):
        post=Post.objects.get(slug=kwargs.get('slug'))
        return post
    '''def get_initial(self):
        post=self.get_queryset()
        initial=super(PostUpdateView,self).get_initial()
        initial['arrival']=post.arrival
        initial['departure']=post.departure
        initial['duration']=post.duration
        initial['title']=post.title
        initial['description']=post.description
        return initial'''

    def get_context_data(self,*args,**kwargs):
        context=super(PostUpdateView,self).get_context_data(*args,**kwargs)
        
        form=PostForm()
        context['post']=Post.objects.get(slug=kwargs.get('slug'))
        context['form']=form
        return context
    def form_valid(self,form):
        post=self.get_queryset()
        post.starting=form.cleaned_data['starting']
        post.ending=form.cleaned_data['ending']
        post.duration=form.cleaned_data['duration']
        post.title=form.cleaned_data['title']
        post.description=form.cleaned_data['description']
        post.save()
        return super(PostUpdateView,self).form_valid(form)
    def get_queryset(self):
        post=Post.objects(slug=self.kwargs.get('slug'))
        return post

class PostDeleteView(DeleteView):
    model=Post
    success_url=reverse_lazy('post-list')
    template_name="posts/post_delete.html"

    def get_queryset(self):
        post=Post.objects(slug=self.kwargs.get('slug'))
        return post


class UserCreationView(FormView):
    model=User
    template_name="register.html"
    form_class=UserRegisterForm

    def get_success_url(self):
        url=reverse_lazy('user_profile',kwargs={'pk',self.object.pk})

    @method_decorator(login_required(login_url='/login'))
    def form_valid(self,loginform): 
        username=form.cleaned_data['username']
        password=form.cleaned_data['password']
        email=form.cleaned_data['email']
        first_name=form.cleaned_data['first_name']
        last_name=form.cleaned_data['last_name']
        user,created=User.objects.get_or_create(username=username,password=password)
        if created:
            user.email=email
            user.first_name=first_name
            user.last_name=last_name
            user.save()
            self.object=user
            return super(UserCreationView,self).form_valid(form)
        else:
            return HttpResponseRedirect("/post/")

    def get_context_data(self,*args,**kwargs):
        self.context=super(UserCreationView,self).get_context_data(*args,**kwargs)
        self.context['loginform']=AuthenticationForm()
        return self.context

def login_view(request):
    if request.method=="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            try:
                user = User.objects.get(username=username)#request.POST['username'])
                if user.check_password(password):#request.POST['password']):
                    user.backend = 'mongoengine.django.auth.MongoEngineBackend'
                    login(request,user)
                    authenticate(username=username,password=password)
                    request.session.set_expiry(60 * 60 * 1) # 1 hour timeout
                    return HttpResponseRedirect("/posts/")#redirect('index')
                else:
                    print "malament"
                    messages.add_message(request,messages.ERROR,u"Incorrect login name or password !")
            except DoesNotExist:
                messages.add_message(request,messages.ERROR,u"Incorrect login name or password !")
                
        else:
            messages.add_message(request,messages.ERROR,u"form not valid")
    else:
        form=AuthenticationForm()
        return render(request, 'login.html', {'form':form})

def user_profile(request,pk):
    user=User.objects(id=pk)
    return render_to_response('posts/profile.html',{'user':user},context_instance=RequestContext(request),)


def create_post(request):
    form=PostForm()
    if request.method=="POST":
        data=PostForm(request.POST)
        if data.is_valid():
            data.save()
            return HttpResponseRedirect('/posts/')
        else:
            errors=u'some errors has been occured'
    else:
        return render_to_response('posts/create.html',context_instance=RequestContext(request),)

def signup(request):
    form=UserCreationForm()
    if request.method=="POST":
        data=UserCreationForm()
        if data.is_valid():
            username=data.cleaned_data['username']
            password=data.cleaned_data['password']
            email=data.cleaned_data['email']
            user=User.objects(username=username,password=password,email=email)
            user.save()
            authenticate(username,password)
            return HttpResponseRedirect('/')
        else:
            errors=u'some errors have been occured'
    return render_to_response('register.html',context_instance=RequestContext(request),)


def plan_post(request,pk,day):
    post=Post.objects.get(id=pk)

