from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from GatePass.settings import COORDINATOR_GROUP, GUARD_GROUP


def login_view(request):
    template = "login.html"
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return goto_user_page(user)
        else:
            context['error'] = 'login error'

    return render(request, template, context)


def login_redirect(request):
    if request.user.is_authenticated():
        return goto_user_page(request.user)
    return login_view(request)


@login_required
def logout_view(request):
    logout(request)
    return login_view(request)


def goto_user_page(user):
    if user.groups.filter(name=COORDINATOR_GROUP).exists():
        return redirect('issue:home')
    elif user.groups.filter(name=GUARD_GROUP).exists():
        return redirect('approve:home')
    elif user.is_superuser:
        return redirect('/admin/')
    elif user.is_authenticated():
        return HttpResponse("You are not assigned any group. Contact the system admin.")
    return HttpResponse("You are already logged in")


@login_required
def home(request):
    return HttpResponse("login successful<a href = '/logout'>")