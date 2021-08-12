from django.contrib import admin
from django.urls import path

from google_oauth.views import CheckGoogle, GoogleOAuthAPIView
from facebook_oauth.views import CheckFacebook, FacebookOAuthAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('google/', CheckGoogle.as_view()),
    path('google/authentication', GoogleOAuthAPIView.as_view()),
    path('facebook/', CheckFacebook.as_view()),
    path('facebook/authentication', FacebookOAuthAPIView.as_view()),
]
