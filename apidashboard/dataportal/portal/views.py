from django.shortcuts import redirect, render, get_object_or_404
from octorest import OctoRest
from .models import Printer , Profile
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout 
from django.contrib.auth.decorators import login_required
from django.views import View
from .printer_views import *
from django.contrib.auth.forms import UserCreationForm
from django.http import StreamingHttpResponse, HttpResponse
import requests

# from .forms import CreateUserForm
from django.contrib.auth.mixins import LoginRequiredMixin

class SignUpView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        form = UserCreationForm()
        return render(request, 'portal/signup.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')
        return render(request, 'portal/signup.html', {'form': form})

class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, 'portal/login.html')

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Username or Password is incorrect')
            return render(request, 'portal/login.html')


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


class IndexView(LoginRequiredMixin, View):
    login_url = 'login'
    # def get(self, request, *args, **kwargs):
    #     printers = Printer.objects.all().values('id', 'ip_address' , 'ping')
    #     return render(request,'portal/portal.html', {'printers': printers})
    def get(self, request, *args, **kwargs):
        user_profile, created = Profile.objects.get_or_create(user=request.user)
        printers = Printer.objects.filter(profile=user_profile).values('id', 'ip_address', 'ping')
        return render(request, 'portal/portal.html', {'printers': printers})

class UserAccountView(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request, *args, **kwargs):
        return render(request,'portal/user_account.html')
class CheckStyle(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request, *args, **kwargs):
        return render(request,'portal/overall_temp/template.html')

class WebcamStreamView(View):
    def get(self, request, printer_id):
        printer = get_object_or_404(Printer, id=printer_id)
        ip_address = printer.ip_address
        if not ip_address.startswith(('http://', 'https://')):
            ip_address = f'http://{ip_address}'
        stream_url = f"{ip_address}/webcam/?action=stream"

        try:
            response = requests.get(stream_url, stream=True)
            return StreamingHttpResponse(
                response.raw,
                content_type=response.headers.get('Content-Type', 'multipart/x-mixed-replace')
            )
        except requests.exceptions.RequestException:
            return HttpResponse("Unable to connect to the printer webcam.", status=502)