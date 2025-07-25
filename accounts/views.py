from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from polls.models import Poll

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
def login_view(request):
    if request.method == 'POST':
        poll_code = request.POST.get('poll_code', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if poll_code:
            try:
                poll = Poll.objects.get(poll_code=poll_code)
                if poll.is_active:
                    return redirect('vote_by_code', code=poll.poll_code)
                else:
                    messages.error(request, '這個投票已經結束或不存在')
            except Poll.DoesNotExist:
                messages.error(request, '無效的投票代碼')
            return render(request, 'accounts/login.html')

        elif username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('polls_index')
            else:
                messages.error(request, '帳號或密碼錯誤')
            return render(request, 'accounts/login.html')

        else:
            messages.error(request, '請輸入帳號與密碼，或投票代碼')

    return render(request, 'accounts/login.html')