from django.contrib import admin
from .models import Borrow,Walet
# Register your models here.

@admin.register(Borrow)
class BookAdmin(admin.ModelAdmin):
    fields=('user', 'book')
    list_display = ('user', 'book', 'borrow_date', 'return_date' , 'fine')

admin.site.register(Walet)