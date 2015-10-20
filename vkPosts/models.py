from django.db import models

# Create your models here.

class Post (models.Model):
    name = models.CharField(max_length= 200, default= 'post')
    direct_link = models.URLField (default= '')

    element_id = models.CharField (max_length=200)
    owner_id = models.IntegerField (default=0)
    post_id = models.IntegerField (default=0)
    post_hash = models.CharField (max_length=200)

    def __str__(self):
        return self.name + ': ' + self.direct_link


    # принимает на вход код для вставки
    # с кавычками ' заменеными на \'
    # НАДО ЭТО ИСПРАВИТЬ

    def setAllAttributes (self, code):
        code = code [code.find('VK.Widgets.Post(') + 'VK.Widgets.Post('.__len__() :
                                                            code.find(', {width')]
        list = code.split(sep=',')
        list[3] = list[3] [1:]
        self.element_id = list[0][1:-1]
        self.owner_id = int(list[1])
        self.post_id = int(list[2])
        self.post_hash = list [3] [1:-1]
