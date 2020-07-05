from django.contrib import admin
from login.models import User, ConfirmString, Interns, RAs

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(ConfirmString)
class ConfirmStringAdmin(admin.ModelAdmin):
    pass

@admin.register(Interns)
class InternsAdmin(admin.ModelAdmin):
    pass

@admin.register(RAs)
class InternsAdmin(admin.ModelAdmin):
    pass