from django.contrib import admin
from . import models

class CustomUserAdmin(admin.ModelAdmin):

    list_display = ["email",]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.

    search_fields = ["email"]
    ordering = ["email"]


admin.site.register(models.CustomUser, CustomUserAdmin)

