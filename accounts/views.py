from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from django.contrib.auth.models import User



def home(request):
    return render(request, 'home.dj')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.address_line1 = form.cleaned_data['address_line1']
            profile.city = form.cleaned_data['city']
            profile.state = form.cleaned_data['state']
            profile.pincode = form.cleaned_data['pincode']
            if form.cleaned_data['profile_picture']:
                profile.profile_picture = form.cleaned_data['profile_picture']
            if request.POST.get('user_type') == 'patient':
                profile.is_patient = True
            else:
                profile.is_doctor = True
            profile.save()
            messages.success(request, 'User created successfully!')
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'signup.dj', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.userprofile.is_patient:
                return redirect('patient_dashboard')
            else:
                return redirect('doctor_dashboard')
    return render(request, 'login.dj')

@login_required
def patient_dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context = {
        'user_profile': user_profile
    }
    return render(request, 'patient_dashboard.dj', context=context)


@login_required
def doctor_dashboard(request):
    return render(request, 'doctor_dashboard.dj')

