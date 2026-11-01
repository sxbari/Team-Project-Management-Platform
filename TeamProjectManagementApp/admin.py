from django.contrib import admin
from .models import Membership, Team
# Register your models here.
admin.site.register(Team)
admin.site.register(Membership)