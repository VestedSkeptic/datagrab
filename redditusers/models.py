from __future__ import unicode_literals

from django.db import models

# Create your models here.
class reddituser(models.Model):
    username = models.CharField(max_length=30)
    
    def __str__(self):
        return format(self.username)    
