from django.contrib import admin
from login.models import User, ConfirmString

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(ConfirmString)
class ConfirmStringAdmin(admin.ModelAdmin):
    pass