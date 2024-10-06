from django import forms
from django.contrib.auth.models import User
from .models import UserProfile  # Import your UserProfile model

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = UserProfile  # Use the UserProfile model to include additional fields
        fields = ['face_id', 'voter_id', 'aadhaar_card', 'age', 'gender']
    
    username = forms.CharField(max_length=150)
    email = forms.EmailField()

    def save(self, commit=True):
        user = User.objects.create_user(username=self.cleaned_data['email'], password="somepassword")
        user_profile = super().save(commit=False)  # Get the user profile
        user_profile.user = user  # Assign the user to the profile
        if commit:
            user_profile.save()
        return user_profile
