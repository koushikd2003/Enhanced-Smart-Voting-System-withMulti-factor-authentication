from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random
from .forms import RegistrationForm
from .models import UserProfile, Vote  # Import Vote model here
from .face_recognition import FaceRecognition  # Import your face recognition class

# Store OTPs in a dictionary with email as key
otp_storage = {}

def HomePage(request):
    return render(request, 'home.html')

def SignupPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            # Create the User object
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            user.save()
            
            # Create the UserProfile object
            user_profile = UserProfile.objects.create(
                user=user,
                face_id=request.POST['face_id'],  # Capture face ID
                voter_id=request.POST['voter_id'],
                aadhaar_card=request.POST['aadhaar_card'],
                age=request.POST['age'],
                gender=request.POST['gender']
            )
            user_profile.save()

            # Store and train the user's face
            addFace(request, user_profile.face_id)  # Store and train face
            
            return redirect('login')  # Redirect to login or another page after successful signup
        
        else:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'signup.html')

    return render(request, 'signup.html')

def addFace(request, face_id):
    """ Add a user's face for future recognition """
    face_recognition = FaceRecognition()  # Create an instance of FaceRecognition
    face_recognition.faceDetect(face_id)  # Call faceDetect on the instance
    face_recognition.trainface()  # Call trainface on the instance
    messages.success(request, "Face registered successfully.")
    return redirect('home')

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            otp_code = random.randint(100000, 999999)
            email = user.email
            otp_storage[email] = otp_code
            
            # Send the OTP via email
            send_mail(
                'Your OTP for Login',
                f'Your OTP is {otp_code}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            
            request.session['username'] = username
            return redirect('otp_verification')
        else:
            messages.error(request, "Username or Password is incorrect!")

    return render(request, 'login.html')

def OtpVerificationPage(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        username = request.session.get('username')

        if username:
            user = User.objects.get(username=username)
            email = user.email

            if otp_storage.get(email) and int(entered_otp) == otp_storage[email]:
                login(request, user)
                otp_storage.pop(email)  # Remove OTP after successful verification
                return redirect('vote')
            else:
                messages.error(request, "Invalid OTP, please try again.")
        else:
            messages.error(request, "Session expired. Please log in again.")

    return render(request, 'otp_verification.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Vote  # Make sure to import your Vote model
from .face_recognition import FaceRecognition
from django.contrib.auth.decorators import login_required

@login_required
def vote_page(request):
    user_profile = request.user.userprofile  # Get the UserProfile of the authenticated user
    
    # Check if the user has already voted
    if Vote.objects.filter(user_profile=user_profile).exists():
        messages.error(request, 'You have already voted.')
        return render(request, 'already_voted.html')
    
    if request.method == 'POST':
        candidate = request.POST.get('candidate')

        if not candidate:
            messages.error(request, 'Please select a candidate to vote.')
            return redirect('vote')  # Redirect to the voting page if no candidate is selected
        
        # Assuming face_id is obtained from the user profile or captured through another method
        face_id = user_profile.face_id  # Assuming this is where you store the face_id
        
        # Verify the user's face
        face_recognition = FaceRecognition()
        if face_recognition.verify(face_id):
            # Save the vote
            Vote.objects.create(user_profile=user_profile, candidate=candidate)
            messages.success(request, 'Your vote has been submitted successfully!')
            return render(request, 'vote_success.html')  # Render a success page
        else:
            messages.error(request, 'Face verification failed. Please try again.')

    return render(request, 'vote.html')  # Render the voting page for GET requests


def verifyFace(face_id):
    """ Verify the user's face for voting """
    face_recognition = FaceRecognition()  # Create an instance of FaceRecognition
    return face_recognition.verify(face_id)  # Assuming there is a method to verify the face

def LogoutPage(request):
    logout(request)
    return redirect('home')
