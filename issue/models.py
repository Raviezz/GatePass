# Create your models here.
from django.contrib.auth.models import User, Group
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.

class Sem(models.Model):
    class Meta:
        db_table = 'sem'
        unique_together = (('frm', 'to', 'no'),)

    sem_id = models.AutoField(primary_key=True)
    frm = models.IntegerField()
    to = models.IntegerField()
    no = models.IntegerField(null=True)

    def __str__(self):
        return str("SEM: " + str(self.no) + " | from " + str(self.frm) + " to " + str(self.to))


class Classes(models.Model):
    class Meta:
        db_table = 'classes'
        unique_together = (('year', 'branch', 'section', 'sem'),)

    class_id = models.AutoField(primary_key=True)
    year = models.IntegerField(
        validators=[MaxValueValidator(4), MinValueValidator(1)]  # use IntegerRangeField when admin enters the years
    )
    branch = models.CharField(max_length=10)
    section = models.CharField(max_length=1, null=True)
    sem = models.ForeignKey(Sem, on_delete=models.CASCADE)

    def __str__(self):
        yearDict = {1: 'I', 2: 'II', 3: 'III', 4: 'IV'}
        if self.section is None:
            sec = ""
        else:
            sec = str(self.section)
        return str(yearDict[self.year] + " " + str(self.branch) + " " + sec)


class Student(models.Model):
    hallticket_no = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=30)
    father_name = models.CharField(max_length=30, null=True)
    student_phno = models.CharField(max_length=15, null=True)
    father_phno = models.CharField(max_length=15, null=True)
    class_id = models.ForeignKey(Classes, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.hallticket_no)


class IssuePass(models.Model):
    issue_id = models.AutoField(primary_key=True)
    issued_by = models.ForeignKey(User, on_delete=models.CASCADE)
    hallticket_no = models.ForeignKey(Student, on_delete=models.CASCADE)
    outTime = models.DateTimeField()
    inTime = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.hallticket_no)

class IssueCancelled(models.Model):
    issue_id = models.ForeignKey(IssuePass, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)


class ApprovePass(models.Model):
    issue_id = models.ForeignKey(IssuePass, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE)
    real_outTime = models.DateTimeField()


class InTimes(models.Model):
    approved_id = models.ForeignKey(ApprovePass, on_delete=models.CASCADE)
    in_time = models.DateTimeField()
