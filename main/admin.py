from django.contrib import admin

from django.contrib import admin
from .models import Transaction


# Register your models here.

class TransactionAdmin(admin.ModelAdmin):
    model = Transaction
    list_display = ['pk', 'name', 'description', 'date_send']
    list_filter = ['description', ]
    list_display_links = ['name', ]
    search_fields = ['description', 'pk']


admin.site.register(Transaction, TransactionAdmin)