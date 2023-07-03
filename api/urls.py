from django.urls import path
from .views import LoginView, RegisterView, SpamView, ContactsView, ProfileView

urlpatterns = [
    path('login/', LoginView.as_view(), name="login-view"),
    path('register/', RegisterView.as_view(), name="resiger-view"),
    path('spam/<str:phone_number>', SpamView.as_view(), name="spam"),
    path('contacts/', ContactsView.as_view(), name="contacts-view"),
    path('profile/<str:id>', ProfileView.as_view(), name="profile-view")
]
