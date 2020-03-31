from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . models import *
from online_users.models import OnlineUserActivity
from django_summernote.admin import SummernoteModelAdmin
from . forms import *

# Summernote for all TextField in model.
class SomeModelAdmin(SummernoteModelAdmin):  
    summernote_fields = ('update')



class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    list_display = ('email', 'user_type', 'department', 'username', 'is_admin')
    list_filter = ('is_admin', 'groups', 'is_active')
    fieldsets = (
        (None, {'fields': ('email',)}),
        ('Personal info', {'fields': ('user_type', 'department','image')}),
        ('Permissions', {'fields': ('is_admin','is_superuser', 'groups', 'user_permissions', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_type', 'department', 'username', 'password1'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)



admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(Updates)
admin.site.register(Comments)
admin.site.site_header = 'Pawame Administration'
