from django.contrib import admin
from .models import Member
from .models import Player

# Register your models here.

class MemberAdmin(admin.ModelAdmin):
	list_display = ('firstname', 'lastname', 'joined_date')

admin.site.register(Member, MemberAdmin)

class PlayerAdmin(admin.ModelAdmin):
	list_display = ('id', 'email')

admin.site.register(Player, PlayerAdmin)
