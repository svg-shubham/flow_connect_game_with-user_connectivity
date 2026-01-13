import json
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .forms import ProfessionalSignupForm
from .models import PlayersProgress

# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        form = ProfessionalSignupForm(request.POST) # Naya form yahan use hoga
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('game:home')
    else:
        form = ProfessionalSignupForm()
    return render(request, 'users/signup.html', {'form': form})
  
def login_view(request):
  if request.method == "POST":
    form = AuthenticationForm(data = request.POST)
    if form.is_valid():
      user = form.get_user()
      login(request,user)
      return redirect("game:home")
  else:
    form = AuthenticationForm()
    return render(request,"users/login.html",{"form":form})
  
def logout_view(request):
  logout(request)
  return redirect("game:home")

@login_required
def save_progress(request):
  if request.method == "POST":
    data = json.loads(request.body)
    print("data yaha tak data aya hain",data)
    # update_or_create use karenge taaki agar user level dobara khele 
    # aur behtar score banaye toh update ho jaye
    PlayersProgress.objects.update_or_create(
       user = request.user,
       level_number = data['level_number'],
       grid_size = data["grid_size"],
       defaults={
                'moves': data['moves'],
                'time_taken': data['time_taken']
            }
            )
    return JsonResponse({"status": "success"})
  return JsonResponse({"status": "failed"}, status=400)

