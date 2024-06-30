import logging

from django.shortcuts import render , redirect
from django.views import View
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login, logout

logger = logging.getLogger('django')

class LoginView(View):
    def get (self, request):
        return render(request, 'userauth/login.html')
    def post (self, request):
        try:
            if request.method =="POST":
                data = request.POST
                username = data.get("username")
                password = data.get("password")
                user = authenticate (request, username=username, password=password)
                if user:
                    login(request,  user)
                return redirect('index')
            return render(request, 'userauth/login.html', {'error': 'Invalid username or password'})
        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return render(request,'userauth/login.html')

    
class LogoutView(View):
    def get (self, request):
        try:
            logout(request)
            return redirect('index')
        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return redirect('index')
