from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.contrib.auth import login, authenticate
from. models import * 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import REDIRECT_FIELD_NAME
from datetime import timedelta
import online_users.models
from .forms import *
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .filters import UserFilter


@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):
    user.profile.is_online = True
    user.profile.save()

@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):
    user.profile.is_online = False
    user.profile.save()


def logins (request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        
        if user is not None:
            login(request, user)
            if  request.user.department == 1 and request.user.is_authenticated:
                return redirect('human_resource')
            elif  request.user.department == 2 and request.user.is_authenticated:
                return redirect('inventory')
            elif request.user.department == 3 and request.user.is_authenticated:
                return redirect('finance')
            elif request.user.department == 4 and request.user.is_authenticated:
                return redirect('marketing')
            elif request.user.department == 5 and request.user.is_authenticated:
                return redirect('information')
            else :
                return redirect('updates')
        else:
            return render(request,'registration/login.html')
    else:
        return render(request,'registration/login.html')
    
@login_required(login_url='/accounts/login/') 
def updates(request):
    updates = Updates.objects.filter(department=1,status=True).all()[::-1]
    num  = Updates.objects.filter(status=False).all().count()
    users = User.objects.order_by('-last_login')
    comments = Comments.objects.all()
    commentForm = CommentForm()
    
    return render(request, 'updates.html', locals())


@user_passes_test(lambda u: u.is_active and u.department==1 or u.user_type==1 ,redirect_field_name=REDIRECT_FIELD_NAME,login_url='login')
def human_resource(request):
    template='human_resource.html'
    updates = Updates.objects.filter(department=2).all()[::-1]
    return render(request,template, {'updates':updates})

@user_passes_test(lambda u:u.is_active and u.department==2 or u.user_type==1,redirect_field_name=REDIRECT_FIELD_NAME,login_url='login')
def inventory(request):
    updates = Updates.objects.filter(department=4).all()[::-1]
    users = User.objects.order_by('-last_login')
    comments = Comments.objects.all()
    commentForm = CommentForm()
    return render(request, 'inventory.html', locals())




@user_passes_test(lambda u:u.is_active and u.department==3 or u.user_type==1,redirect_field_name=REDIRECT_FIELD_NAME,login_url='login')
def finance(request):
    template='finance.html'
    updates = Updates.objects.filter(department=6).all()[::-1]
    return render(request,template,{'update':updates})


@user_passes_test(lambda u:u.is_active and u.department==4 or u.user_type==1,redirect_field_name=REDIRECT_FIELD_NAME,login_url='login')
def marketing(request):
    template='marketing.html'
    updates = Updates.objects.filter(department=5).all()
    return render(request, template,{'updates':updates})

@user_passes_test(lambda u:u.is_active and u.department==5 or u.user_type==1,redirect_field_name=REDIRECT_FIELD_NAME,login_url='login')
def information_technology(request):
    template='information_technology.html'
    updates = Updates.objects.filter(department=3).all()[::-1]
    return render(request,template,{'update':updates})

# @login_required(login_url='accounts/login')
def employees(request):
    user_status = online_users.models.OnlineUserActivity.get_user_activities(timedelta(minutes=60))
    users = (user for user in user_status)
    context = {"online_users"}

    if request.user.user_type == 1 or request.user.user_type == 2:
        return render(request, 'employees.html')
    else:
        return render(request, 'employeeProfile.html')


def notifications(request):
    template='notifications.html'
    updates=Updates.objects.filter(status=False).all()[::-1]
    num  = Updates.objects.filter(status=False).all().count()
    return render(request, template, locals())
    

def employeeProfile(request):
    current_user = request.user
    profile = Profile.objects.filter(user= current_user)
    return render(request, 'employeeProfile.html', {'profile':profile})


# @login_required(login_url='accounts/login')
def postUpdate(request):
    current_user =  request.user
    if current_user.user_type == 1 or current_user.user_type==2:
        if request.method == 'POST':
            form = PostUpdateForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = current_user
                post.save()
            return redirect('updates')
        else:
            form = PostUpdateForm()
            return render(request, 'postUpdate.html', {"form":form})
    return redirect('updates')
  
def searchResults(request):
    
    if 'employee' in request.GET and request.GET["employee"]:

        search_term = request.GET.get("employee")
        searched_employees = User.search_employees(search_term)
        message = f"{search_term}"
        return render(request, 'searchResults.html', {"message": message, "Employees": searched_employees})
    else:
        message = "You haven't searched for any term "
        return render(request, 'searchResults.html', {"message": message})
     

#comments
@login_required(login_url='/accounts/login')
def comments(request, update_id):
    commentForm = CommentForm()
    update = get_object_or_404(Updates,pk=update_id)
        
    if request.method == 'POST':
        commentForm = CommentForm(request.POST)
        if commentForm.is_valid():            
            form = commentForm.save(commit=False)
            form.user=request.user
            form.update=get_object_or_404(Updates,pk=update_id)
            form.save()
        return redirect ('updates')
    return render (request, 'updates.html', locals())

def approved(request, id):
    Updates.approved(id)
    return redirect('notifications')

