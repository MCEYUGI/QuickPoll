from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='polls_index'),
    path('create/', views.create_poll),
    path('poll/<int:poll_id>/', views.poll_detail, name='poll_detail'),
    path('poll/<int:poll_id>/vote/', views.poll_vote, name='poll_vote'),
    # 其他可能的 URL 路由
]
