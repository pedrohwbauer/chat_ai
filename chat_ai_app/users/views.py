from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('chat:index')  # Redirect to the chat index page
    else:
        form = UserCreationForm()
        
    return render(request, 'registration/register.html', {'form': form})