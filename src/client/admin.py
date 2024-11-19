from django.contrib import admin
from .models import ClientModel


# Register your models here.
class ClientAdmin(admin.ModelAdmin):
    list_filter = ['nomCompletClient']


admin.site.register(ClientModel, ClientAdmin)
