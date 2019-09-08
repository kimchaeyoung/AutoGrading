from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import *

class ProfessorAdmin(admin.ModelAdmin):
    list_per_page= 5
    list_display = ('professor_id', 'professor_name', 'status')
    list_editable = ('status',)
    
    actions = ['setPermission']

    def setPermission(self, request, queryset):
        for professor in queryset:
            Professor.objects.filter(professor_name=professor.professor_name).update(status=True)
        messages.success(request, '{0}명의 교수를 인증했습니다.'.format(len(queryset)))

    setPermission.short_description = "선택한 교수의 관리자 권한 부여"
  
admin.site.register(Student) 
admin.site.register(Professor, ProfessorAdmin) 
        
