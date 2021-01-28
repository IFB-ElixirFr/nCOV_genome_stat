from django.urls import path, include

from home.views import home, register, thanks, contact

urlpatterns = [
    path("", home, name="home_page"),
    path("signUp/", register, name='signUp'),
    path("contact/", contact, name='contact'),
    path("thanks/<str:userName>/", thanks, name='thanks'),
]

