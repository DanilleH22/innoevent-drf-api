from django.urls import path
from events import views

urlpatterns = [
    path('events/', views.EventList.as_view()),
    path('events/create', views.EventCreate.as_view()),
    path('events/<int:pk>/', views.EventDetail.as_view()),
]