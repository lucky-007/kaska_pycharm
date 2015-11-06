from django.db import models


# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length= 50)
    #Поле для хранения пулов тех игроков, которые уже в команде
    def __str__(self):
        return self.name
