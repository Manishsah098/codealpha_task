from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('events/', views.EventList.as_view(), name='event-list'),
    path('events/<int:pk>/', views.EventDetail.as_view(), name='event-detail'),
    path('registrations/', views.RegistrationList.as_view(), name='registration-list'),
    path('registrations/<int:pk>/', views.RegistrationDetail.as_view(), name='registration-detail'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('me/', views.UserDetailView.as_view(), name='user-detail'),
]
