from django.contrib import admin

# Register your models here.
from .models import Desks, CompanyName, Profile

#admin.site.register(Desks)

#admin.site.register(Profile)

#admin.site.register(CompanyName)

@admin.register(CompanyName)
class CompanyNameAdmin(admin.ModelAdmin):
    list_display = ('name','id')

@admin.register(Desks)
class DesksAdmin(admin.ModelAdmin):
    list_display = ('id','due_date','task','company_name')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','active_company','idsession')
