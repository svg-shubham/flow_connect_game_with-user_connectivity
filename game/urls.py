from django.urls import path
from . import views

app_name = 'game'
urlpatterns = [
    path('', views.home_view, name='home'),
    path('levels/<int:size>/', views.level_selection_view, name='level_list'),
    path('get_level/', views.get_level_data, name='get_level_data'),
    path('play_game/<int:size>/<int:level>/', views.play_level, name='play_level')
]