from django.contrib import admin
from .models import Membership, Tasks, Team
# Register your models here.
admin.site.register(Team)
admin.site.register(Membership)
admin.site.register(Tasks)