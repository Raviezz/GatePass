from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from GatePass.settings import COORDINATOR_GROUP, GUARD_GROUP
from issue.models import *


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
    template = 'issue/home.html'
    context = {}

    if request.method == 'POST':
        if 'search' in request.POST:
            try:

                student_id = Student.objects.get(hallticket_no=request.POST.get('studid'))
                request.session['student_id'] = student_id.hallticket_no
                context['student'] = student_id
            except:
                context['error'] = "not found"

        if 'submit' in request.POST:
            #try:
                outtime = datetime.now()
                inTime = request.POST.get('inTime')
                reason = request.POST.get('reason')
                IssuePass.objects.create(issued_by=request.user, hallticket_no=Student.objects.get(hallticket_no=request.session.get('student_id')),
                                         outTime=outtime
                                         , inTime=inTime, reason=reason)
            #except:
                context['error'] = "wrong input"


    all_issues=IssuePass.objects.all()
    stud_list=[]
    for s in all_issues:
        if s not in IssueCancelled.objects.all():
            stud_list.append(s)

    context['all_students']=stud_list
    return render(request, template, context)
