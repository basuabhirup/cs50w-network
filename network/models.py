from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  content = models.TextField()
  timestamp = models.DateTimeField(auto_now_add=True)
  likes = models.PositiveIntegerField(default=0)
  
  def __str__(self):
    return f"{self.user.username}: {self.content} - at {self.timestamp} - with {self.likes} likes."

class Follower(models.Model):
  follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
  following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

  class Meta:
    unique_together = ('follower', 'following')
    
    
class Like(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked_posts")
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked_by")
  timestamp = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = ('user', 'post')