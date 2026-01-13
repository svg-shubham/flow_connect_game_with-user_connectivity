from django.urls import path
from .views import *

app_name = 'user'
urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('save-progress/', save_progress, name='save_progress'),
]