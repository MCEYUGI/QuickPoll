from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        if password1 != password2:
            messages.error(request, '密碼不一致')
            return render(request, 'accounts/signup.html')
        if User.objects.filter(username=username).exists():
            messages.error(request, '帳號已存在')
            return render(request, 'accounts/signup.html')
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, '註冊成功，請登入')
        return redirect('login')
        
    return render(request, 'accounts/signup.html')