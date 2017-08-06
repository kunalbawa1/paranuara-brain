from django.contrib import admin
from paranuara.models import *

# Register your models here.
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('index', 'name')

class PersonAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'age', 'died')

admin.site.register(Company, CompanyAdmin)
admin.site.register(Person, PersonAdmin)