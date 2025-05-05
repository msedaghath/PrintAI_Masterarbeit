from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import UserProfileForm
from django.contrib.auth.models import User


class SignUpView(View):
    """View for user registration"""
    template_name = 'accounts/signup.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # No need to create a profile anymore
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account was created for {username}')
            return redirect('login')
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    """View for user login"""
    template_name = 'accounts/login.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, self.template_name)


@login_required(login_url='login')
def logout_user(request):
    """View for user logout"""
    logout(request)
    return redirect('login')


class UserAccountView(LoginRequiredMixin, View):
    """View for user profile management"""
    template_name = 'accounts/user_account.html'
    login_url = 'login'
    
    def get(self, request, *args, **kwargs):
        form = UserProfileForm(instance=request.user)
        return render(request, self.template_name, {'form': form})
        
    def post(self, request, *args, **kwargs):
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('user_account')
        return render(request, self.template_name, {'form': form})