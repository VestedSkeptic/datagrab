from __future__ import unicode_literals

from django.db import models

# Create your models here.
class reddituser(models.Model):
    username = models.CharField(max_length=30)
    commentsafter = models.CharField(max_length=30, default="", blank=True, null=True)
    
    def __str__(self):
        return format(self.username + " " + self.commentsafter)    
