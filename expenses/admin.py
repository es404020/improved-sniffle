from django.contrib import admin
from expenses.models import User, Expense

admin.site.register(User)
admin.site.register(Expense)