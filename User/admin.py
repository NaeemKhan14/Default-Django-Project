from django.contrib import admin

# Register your models here.
from User.models import UserAccount

admin.site.register(UserAccount)
