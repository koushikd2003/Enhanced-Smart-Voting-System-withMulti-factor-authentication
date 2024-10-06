from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    face_id = models.CharField(max_length=100)
    voter_id = models.CharField(max_length=20)
    aadhaar_card = models.CharField(max_length=12)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username

class Vote(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    candidate = models.CharField(max_length=255)
    date_voted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_profile.user.username} voted for {self.candidate}"
