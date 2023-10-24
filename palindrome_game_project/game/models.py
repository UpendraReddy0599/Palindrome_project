from django.db import models

# Create your models here.

class Game(models.Model):
    game_id = models.CharField(max_length=10, unique=True)
    string = models.CharField(max_length=50)
