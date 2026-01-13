from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import GameLevel
from django.core.paginator import Paginator
from users.models import PlayersProgress

# Create your views here.
# game_app/views.py
from django.shortcuts import render
import json

def landing_page(request):
    return render(request, 'game/landing.html')

def home_view(request):
    # Home page par humein sirf categories dikhani hain
    return render(request, 'game/home.html')

def level_selection_view(request, size):
    levels = GameLevel.objects.filter(grid_size=size).order_by('level_number')
    completed_levels = PlayersProgress.objects.filter(
        user=request.user, 
        grid_size=size
    ).values_list('level_number', flat=True)
    paginator = Paginator(levels,20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    labels = {5: "Beginner", 6: "Medium", 8: "Hard"}
    return render(request, 'game/level_selection.html', {
        'levels': page_obj,
        'size': size,
        'difficulty_label': labels.get(size, "Unknown"),
        'completed_levels': completed_levels,
    })

def play_level(request, size, level):
    try:
        level_obj = GameLevel.objects.get(grid_size=size, level_number=level)
        dot_config = level_obj.dot_configuration
    except GameLevel.DoesNotExist:
        return redirect('game:home')

    context = {
        'size': size,
        'level': level,
        'dot_config_json': json.dumps(dot_config), 
    }
    return render(request, 'game/play.html', context)

def get_level_data(request):
    # JS se strings aati hain, isliye inhe fetch karo
    size_str = request.GET.get('size')
    level_str = request.GET.get('level')

    try:
        # String ko Integer mein convert karna zaroori hai model filtering ke liye
        size = int(size_str)
        level = int(level_str)

        # Model se data uthao
        level_obj = GameLevel.objects.get(grid_size=size, level_number=level)
        
        # 'dot_configuration' wahi hai jo aapke model mein hai
        return JsonResponse({
            'status': 'success',
            'dots': level_obj.dot_configuration 
        })

    except (GameLevel.DoesNotExist, ValueError, TypeError):
        return JsonResponse({
            'status': 'error', 
            'message': f'Level {level_str} for size {size_str} not found in database.'
        }, status=404)
    except Exception as e:
        # Agar koi aur error aaye (jaise spelling mistake) toh wo yahan dikhegi
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500) 