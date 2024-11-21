from django.contrib import admin
from BookApp.models import BookModel, BorrowModel

# Register your models here.
admin.site.register(BookModel)
admin.site.register(BorrowModel)