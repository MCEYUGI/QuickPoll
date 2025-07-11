from django.shortcuts import render, redirect
# render: 用來渲染模板並回傳 HTML。
from django.contrib.auth.decorators import login_required
# login_required: 裝飾器，限制未登入的使用者存取該 view
from .models import Poll, Vote, Option
# .models: 引入 Poll（投票主題）與 Vote（使用者的投票紀錄）模型
# Create your views here.

@login_required
def index(request):
    # 使用者新增的主題
    user_polls = Poll.objects.filter(created_by=request.user).order_by('-created_at')[:5] # 顯示最新的五筆新增主題紀錄
    user_votes = Vote.objects.filter(voter_id=request.user.username).order_by('-voted_at').select_related('poll', 'option')[:5] # 顯示最新的五筆投票紀錄
    public_polls = Poll.objects.filter(is_public=True, is_active=True).order_by('-created_at')[:10]

    context = {
        'user_polls':user_polls,
        'user_votes':user_votes,
        'public_polls':public_polls,
    }
        
    return render(request, 'polls/index.html', context)

@login_required
def create_poll(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        is_public = request.POST['is_public'] == 'True'
        created_by = request.user

        # 1. 先建立 Poll
        poll = Poll.objects.create(
            title=title,
            description=description,
            created_by=created_by,
            is_public=is_public
        )

        # 2. 再建立 Option（多個）
        options = request.POST.getlist('options')
        for option_text in options:
            if option_text.strip():
                option = Option.objects.create(
                    poll=poll,
                    text=option_text.strip()
                )
        # 3. 完成後導回首頁或顯示訊息
        return redirect('polls_index')
#I want to know which language is well known and people often use more in common place
#Which language is best?