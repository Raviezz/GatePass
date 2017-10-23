from django.contrib import admin
from issue.models import  *
# Register your models here.
admin.site.register(Sem),
admin.site.register(Classes),
admin.site.register(Student),
admin.site.register(IssuePass)