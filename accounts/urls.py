from accounts.views import RegisterApiView
from django.urls import path

urlpatterns = [
    path('register/', RegisterApiView.as_view()),
]