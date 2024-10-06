from django.urls import path
from .views import HomePage, SignupPage, LoginPage, LogoutPage, OtpVerificationPage, vote_page

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', HomePage, name='home'),
    path('signup/', SignupPage, name='signup'),
    path('login/', LoginPage, name='login'),
    path('logout/', LogoutPage, name='logout'),
    path('otp_verification/', OtpVerificationPage, name='otp_verification'),
    path('vote/', vote_page, name='vote'),
    # path('submit_vote/', submit_vote, name='submit_vote'),  # Add this line # OTP verification path
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
