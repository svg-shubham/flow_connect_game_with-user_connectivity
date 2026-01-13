from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PlayersProgress(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  level_number = models.IntegerField()
  grid_size = models.IntegerField()
  moves = models.IntegerField()
  time_taken = models.IntegerField()#litne seconds main hua hain
  completed_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = ('user','level_number','grid_size')

  def __str__(self):
    return f"{self.user.username}-gird{self.grid_size} - Level {self.level_number}"



