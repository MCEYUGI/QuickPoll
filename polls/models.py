from django.db import models
from django.utils.crypto import get_random_string

def generate_poll_code():
    return get_random_string(length=6)
# Create your models here.
class Poll(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    poll_code = models.CharField(max_length=6, default=generate_poll_code, unique=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Option(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.text
    
class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    voter_id = models.CharField(max_length=100)  # 可是帳號、代碼、IP...
    voted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.voter_id} voted for {self.option}"
