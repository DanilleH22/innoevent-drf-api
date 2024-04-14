from django.urls import path
from contact import views

urlpatterns = [
    path('contact_us/', views.ContactUs.as_view()),
]