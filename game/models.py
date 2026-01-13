from django.db import models

# Create your models here.

class GameLevel(models.Model):
  DIFFICULTY_CHOICES = [
        (5, 'Beginner (5x5)'),
        (6, 'Medium (6x6)'),
        (8, 'Hard (8x8)'),
    ]
  grid_size = models.IntegerField(choices=DIFFICULTY_CHOICES,default=5)
  level_number = models.IntegerField()
  dot_configuration = models.JSONField(help_text="Paste your JSON dot config here")
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = ('grid_size', 'level_number')
    ordering = ['grid_size', 'level_number']

  def __str__(self):
        return f"{self.grid_size}x{self.grid_size} - Level {self.level_number}"
