from django.shortcuts import render, redirect, get_object_or_404
# render: 用來渲染模板並回傳 HTML。
from django.contrib.auth.decorators import login_required
# login_required: 裝飾器，限制未登入的使用者存取該 view
from .models import Poll, Vote, Option
# .models: 引入 Poll（投票主題）與 Vote（使用者的投票紀錄）模型
from django.contrib import messages
# messages: 用來顯示訊息給使用者，例如註冊成功或密碼不一致等錯誤訊息。
from django.contrib.auth.models import User
# Create your views here.

@login_required
def index(request):
    # 使用者新增的主題
    user_polls = Poll.objects.filter(created_by=request.user).order_by('-created_at')[:5] # 顯示最新的五筆新增主題紀錄
    user_votes = Vote.objects.filter(voter_id=request.user.id).order_by('-voted_at').select_related('poll', 'option')[:5] # 顯示最新的五筆投票紀錄
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

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip   

def vote_by_code(request, code):
    poll = get_object_or_404(Poll, poll_code=code)
    voter_ip = get_client_ip(request) # 獲取投票者的 IP 地址
    # 檢查是否投過票了
    has_voted = Vote.objects.filter(poll=poll, voter_id=voter_ip).exists()
    if has_voted:
        messages.error(request, '您已經投過票了，無法再次投票。')
        return redirect('poll_detail', poll_id=poll.id)
    #檢查投票是否已結束
    if not poll.is_active:
        messages.error(request, '此投票已結束，無法投票。')
        return redirect('poll_detail', poll_id=poll.id)
    if request.method == 'POST':
        option_id = request.POST.get('option_id')
        option = get_object_or_404(Option, id=option_id, poll=poll)
        Vote.objects.create(poll=poll, option=option, voter_id=voter_ip)
        option.votes += 1
        option.save()
        messages.success(request, '投票成功！請回首頁。')
        return redirect('poll_detail', poll_id=poll.id)
    return redirect('poll_detail', poll_id=poll.id)

def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    total_votes = sum([option.votes for option in poll.options.all()])
    best_option = poll.options.order_by('votes').last()  # 獲取得票最多的選項
    if request.user.is_authenticated:
        has_voted = Vote.objects.filter(poll=poll, voter_id=str(request.user.id)).exists()
        return render(request, 'polls/poll_detail.html', {'poll': poll, 'has_voted': has_voted, 'total_votes': total_votes, 'best_option': best_option})
    else:
        has_voted = Vote.objects.filter(poll=poll, voter_id=get_client_ip(request)).exists()
        return render(request, 'polls/poll_detail.html', {'poll': poll, 'has_voted': has_voted, 'total_votes': total_votes, 'best_option': best_option})

@login_required
def poll_vote(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    # 檢查是否投過票了
    has_voted = Vote.objects.filter(poll=poll, voter_id=str(request.user.id)).exists()
    if has_voted:
        messages.error(request, '您已經投過票了，無法再次投票。')
        return redirect('poll_detail', poll_id=poll.id)
    #檢查投票是否已結束
    if not poll.is_active:
        messages.error(request, '此投票已結束，無法投票。')
        return redirect('poll_detail', poll_id=poll.id)
    if request.method == 'POST':
        option_id = request.POST.get('option_id')
        option = get_object_or_404(Option, id=option_id, poll=poll)
        Vote.objects.create(poll=poll, option=option, voter_id=str(request.user.id))
        option.votes += 1
        option.save()
        messages.success(request, '投票成功！請回首頁。')
        return redirect('poll_detail', poll_id=poll.id)
    return redirect('poll_detail', poll_id=poll.id)