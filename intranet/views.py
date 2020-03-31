from django.http import JsonResponse
from django.utils.http import is_safe_url
from .filters import UserFilter
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from .forms import *
import online_users.models
from datetime import timedelta
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.contrib.auth import login, authenticate
from. models import *
from django.contrib import messages


@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):
    user.is_online = True
    user.save()

@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):
    user.is_online = False
    user.save()


def logins(request):
    
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email)
        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
            print(request.user.user_type)
            if request.user.department == 1 and request.user.is_authenticated:
                return redirect('human_resource')
            elif request.user.department == 2 and request.user.is_authenticated:
                return redirect('inventory')
            elif request.user.department == 3 and request.user.is_authenticated:
                return redirect('finance')
            elif request.user.department == 4 and request.user.is_authenticated:
                return redirect('marketing')
            elif request.user.department == 5 and request.user.is_authenticated:
                return redirect('information')
            else:
                return redirect('updates')
        else:
            return render(request, 'registration/login.html')
    else:
        return render(request, 'registration/login.html')


@login_required(login_url='/accounts/login/')
def updates(request):
    updates = Updates.objects.filter(department=1, status=True).all()[::-1]
    num = Updates.objects.filter(status=False).all().count()
    users = User.objects.order_by('-last_login')
    comments = Comments.objects.all()
    commentForm = CommentForm()

    return render(request, 'updates.html', locals())


@user_passes_test(lambda u: u.is_active and u.department == 1 or u.user_type == 1, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login')
def human_resource(request):
    template = 'human_resource.html'
    updates = Updates.objects.filter(department=2 , status=True).all()[::-1]
    commentForm = CommentForm()
    users = User.objects.order_by('-last_login')
    num = Updates.objects.filter(status=False).all().count()
    return render(request, template, locals())

@user_passes_test(lambda u: u.is_active and u.department == 2 or u.user_type == 1, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login')
def inventory(request):
    updates = Updates.objects.filter(department=4 , status=True).all()[::-1]
    num = Updates.objects.filter(status=False).all().count()
    users = User.objects.order_by('-last_login')
    commentForm = CommentForm()
    return render(request, 'inventory.html', locals())


@user_passes_test(lambda u: u.is_active and u.department == 3 or u.user_type == 1, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login')
def finance(request):
    template = 'finance.html'
    updates = Updates.objects.filter(department=6 , status=True).all()[::-1]
    commentForm = CommentForm()
    users = User.objects.order_by('-last_login')
    num = Updates.objects.filter(status=False).all().count()
    return render(request, 'finance.html', locals())


@user_passes_test(lambda u: u.is_active and u.department == 4 or u.user_type == 1, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login')
def marketing(request):
    template = 'marketing.html'
    updates = Updates.objects.filter(department=5 , status=True).all()
    commentForm = CommentForm()
    users = User.objects.order_by('-last_login')
    num = Updates.objects.filter(status=False).all().count()
    return render(request, 'marketing.html', locals())


@user_passes_test(lambda u: u.is_active and u.department == 5 or u.user_type == 1, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login')
def information_technology(request):
    template = 'information_technology.html'
    updates = Updates.objects.filter(department=3 , status=True).all()[::-1]
    commentForm = CommentForm()
    users = User.objects.order_by('-last_login')
    num = Updates.objects.filter(status=False).all().count()
    return render(request, 'information_technology.html', locals())


# @login_required(login_url='accounts/login')
def employees(request):
    user_status = online_users.models.OnlineUserActivity.get_user_activities(
        timedelta(minutes=60))
    users = (user for user in user_status)
    onusers = User.objects.order_by('-last_login')
    num = Updates.objects.filter(status=False).all().count()
    context = {"online_users"}

    if request.user.user_type == 1 or request.user.user_type == 2:
        return render(request, 'employees.html', locals())
    else:
        return render(request, 'employeeProfile.html', locals())


@login_required(login_url='/accounts/login/')
def notifications(request):
    template = 'notifications.html'
    updates = Updates.objects.filter(status=False).all()[::-1]
    users = User.objects.order_by('-last_login')
    num = Updates.objects.filter(status=False).all().count()
    return render(request, template, locals())


def employeeProfile(request):
    current_user = request.user
    profile = Profile.objects.filter(user=request.user)
    num = Updates.objects.filter(status=False).all().count()
    return render(request, 'employeeProfile.html', locals())


def editProfile(request):
    editProfileForm = EditProfileForm()
    current_user = request.user
    profile = Profile.objects.filter(user=current_user)
    num = Updates.objects.filter(status=False).all().count()
    
    return render(request, 'editProfile.html', locals())
    

#updatePic
@login_required(login_url='/accounts/login')
def updateProfilePic(request):
    editProfileForm = EditProfileForm(instance=request.user)
    if request.method == 'POST':
        editProfileForm = EditProfileForm(request.POST,request.FILES,instance=request.user)

        if editProfileForm.is_valid():
            editProfileForm.save()
            return redirect('employeeProfile')
    else:
        editProfileForm = EditProfileForm(instance=request.user)

    return render(request,'editProfile.html', locals())


# @login_required(login_url='accounts/login')
def postUpdate(request):
    current_user = request.user
    num = Updates.objects.filter(status=False).all().count()
    if current_user.user_type == 1 or current_user.user_type == 2:
        if request.method == 'POST':
            form = PostUpdateForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = current_user
                post.save()
                dep = ['updates', 'human_resource', 'information', 'inventory', 'marketing', 'finance']
                messages.success(request, 'Submission successful. Update awaiting approval before being published')
                print(messages, '================================')
                return redirect(dep[post.department-1])
        else:
            form = PostUpdateForm()
            return render(request, 'postUpdate.html', locals())
    return redirect('updates')


def searchResults(request):
    num = Updates.objects.filter(status=False).all().count()
    if 'employee' in request.GET and request.GET["employee"]:

        search_term = request.GET.get("employee")
        searched_employees = User.search_employees(search_term)
        message = f"{search_term}"
        num = Updates.objects.filter(status=False).all().count()
        return render(request, 'searchResults.html', {"message": message, "Employees": searched_employees , "num": num})
    else:
        message = "You haven't searched for any term"
        return render(request, 'searchResults.html', {"message": message, "num": num})


# comments
@login_required(login_url='/accounts/login')
def comments(request, update_id):
    commentForm = CommentForm()
    update = get_object_or_404(Updates, pk=update_id)
    dynamic_path = request.get_full_path        
    num = Updates.objects.filter(status=False).all().count()

    if request.method == 'POST':
        commentForm = CommentForm(request.POST)
        if commentForm.is_valid():
            form = commentForm.save(commit=False)
            form.user = request.user
            form.update = get_object_or_404(Updates, pk=update_id)
            form.save()            
            next_url = request.POST.get('next')
            if not next_url or not is_safe_url(url=next_url, allowed_hosts=request.get_host()):
                next_url = reverse('updates')
            return HttpResponseRedirect(next_url) 
    
#commenting per update
@login_required(login_url='/accounts/login')
def commenting (request, update_id):
    commentForm = CommentForm()
    update = get_object_or_404(Updates, pk=update_id)
    num = Updates.objects.filter(status=False).all().count()
    users = User.objects.order_by('-last_login')
    
    if request.method == 'POST':
        commentForm = CommentForm(request.POST)
        if commentForm.is_valid():
            form = commentForm.save(commit=False)
            form.user = request.user
            form.update = get_object_or_404(Updates, pk=update_id)
            form.save()            
            next_url = request.POST.get('next')
            if not next_url or not is_safe_url(url=next_url, allowed_hosts=request.get_host()):
                next_url = reverse('updates')
            return HttpResponseRedirect(next_url)  
    else:
        commentForm = CommentForm()
        return render(request, 'commenting.html', locals())
    

def approved(request, id):
    Updates.approved(id)
    return redirect('notifications')

def disapproved(request, id):
    Updates.dissaprove(id)
    return redirect('notifications')

def delete_employee(request,id):
    query = User.objects.get(pk=id)
    query.delete()
    return redirect("employees")


