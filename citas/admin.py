from django.contrib import admin
from .models import CustomUser, Proyecto, Cita
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role')  # Añade los campos que quieres mostrar
    list_filter = ('role',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Proyecto)
admin.site.register(Cita)
