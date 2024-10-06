from django.contrib import admin
from .models import UserProfile, Vote

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'voter_id', 'age', 'gender')  # Adjust as needed

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('candidate',)  # Display these fields in the admin
    search_fields = ('candidate',) 
