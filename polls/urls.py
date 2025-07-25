from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='polls_index'),
    path('create/', views.create_poll, name='poll_create'),

    # 透過 ID 操作投票
    path('poll/<int:poll_id>/', views.poll_detail, name='poll_detail'),
    path('poll/<int:poll_id>/vote/', views.poll_vote, name='poll_vote'),

    # 透過投票代碼（code）匿名投票
    path('vote/<str:code>/', views.vote_by_code, name='vote_by_code'),
]
