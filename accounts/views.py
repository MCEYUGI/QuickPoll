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
        username = request.POST['username']
        password = request.POST['password']
        poll_code = request.POST.get('poll_code')
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('polls_index')
            else:
                messages.error(request, '帳號或密碼錯誤')
                return render(request, 'accounts/login.html')
        elif poll_code:
            # 處理poll_code登入邏輯
            try: 
                poll = Poll.objects.get(poll_code=poll_code) # 查詢是否有這個投票代碼
                if poll.is_active: # 如果這個投票是啟用的
                    return redirect('poll_detail', poll_id=poll.id)
                else:
                    messages.error(request, '這個投票已經結束或不存在')
                    return render(request, 'accounts/login.html')
            except Poll.DoesNotExist:
                messages.error(request, '無效的投票代碼')
                return render(request, 'accounts/login.html')
    return render(request, 'accounts/login.html')