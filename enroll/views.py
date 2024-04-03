# authentication_app/views.py

from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to dashboard if the user is a superuser
                if user.is_superuser:
                    return redirect('dashboard')
                else:
                    # Redirect to another page if the user is not a superuser
                    return redirect('some_other_page')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

from django.contrib.auth.models import User
from .models import MyDataModel

@permission_required('enroll.can_view_data')
def view_data(request):
    if request.user.has_perm('enroll.can_view_data'):
        user_data = MyDataModel.objects.filter(user=request.user)
        return render(request, 'view_data.html', {'user_data': user_data})
    else:
        return HttpResponse("You don't have permission to view this data.")


def custom_password_reset(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            # Redirect to the password reset done page
            return redirect('password_reset_done')
    else:
        form = PasswordResetForm()
    return render(request, "password_reset.html", {'form': form})

def custom_password_reset_done(request):
    return render(request, "password_reset_done.html")

def custom_logout(request):
    logout(request)
    return redirect('login')




# enroll/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import LoginForm
def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user, created = User.objects.get_or_create(username=email, email=email)
            if created:
                user.set_password('user@123')
                user.save()
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  
            else:
                return render(request, 'userlogin.html', {'form': form, 'error_message': 'Invalid email or password.'})
    else:
        form = LoginForm()
    return render(request, 'userlogin.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile

@login_required
def user_info(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile, _ = Profile.objects.get_or_create(user=request.user)
            profile.ups_name = form.cleaned_data['ups_name']
            profile.ups_serial_number = form.cleaned_data['ups_serial_number']
            profile.address = form.cleaned_data['address']
            profile.save()
            return redirect('dashboard')
    else:
        form = ProfileForm()
    return render(request, 'userinfo.html', {'user_info_form': form})

