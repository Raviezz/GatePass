from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from issue.models import *


@login_required
def home(request):
    template = 'approve/home.html'
    context = {}



    if request.method =='POST':
        if 'approve' in request.POST:
            issue_id = request.POST['approve']
            issue = IssuePass.objects.get(issue_id=issue_id)
            ApprovePass.objects.create(issue_id=issue, approved_by=request.user)

        if 'return' in request.POST:
            issue_id = request.POST['return']
            issue = IssuePass.objects.get(issue_id=issue_id)
            for approve in ApprovePass.objects.all():
                if approve.issue_id == issue:
                    InTimes.objects.create(approved_id=approve)
                    break

    approved_passes = ApprovePass.objects.all()
    approved_students = []
    inTimes3 = InTimes.objects.all()
    inTimes = [x.approved_id for x in inTimes3]

    for pas in approved_passes:
        if pas not in inTimes:
            approved_students.append(pas.issue_id.hallticket_no.hallticket_no)

    context['approved_students'] = approved_students

    inTime2=[x.issue_id for x in inTimes]

    all_issues = IssuePass.objects.all()
    stud_list = []
    for s in all_issues:
        if s not in IssueCancelled.objects.all() and s not in inTime2 :
            stud_list.append(s)

    history = []
    for inTime in inTimes3:
        history.append(inTime)

    context['history'] = history

    context['all_students'] = stud_list
    return render(request, template, context)


