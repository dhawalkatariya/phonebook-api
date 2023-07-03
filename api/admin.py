from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import UserAdmin
from .models import User, Contact, Spam
from .forms import CreateUserForm, EditUserForm


class UserAdmin(BaseUserAdmin):
    add_form = CreateUserForm
    form = EditUserForm
    list_display = ['name', 'email', 'phone_number']
    search_fields = ('name', 'email', 'phone_number')
    list_per_page = 20
    fieldsets = (
        (None, {"fields": ("phone_number", "password", "email", "name")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "phone_number", "name", "emai", "password1", "password2"
            )}
         ),
    )
    ordering=('phone_number',)


admin.site.register(User, UserAdmin)

admin.site.register(Contact)
admin.site.register(Spam)
