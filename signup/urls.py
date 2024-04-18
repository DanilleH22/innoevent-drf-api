from django.urls import path
from signup import views

urlpatterns = [
    path('events/<int:pk>/signup/', views.EventSignUp.as_view()),
]