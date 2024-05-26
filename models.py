from django.db import models
from django.contrib.auth.models import User
from document.models import *

class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_date = models.CharField(max_length=40)
    branch = models.CharField(max_length=30)
    subject = models.CharField(max_length=30)
    notesfile = models.FileField(null=True)
    filetype = models.CharField(max_length=40)
    status = models.CharField(max_length=50)
    year = models.CharField(max_length=30)
    
    def __str__(self):
        return f"{self.user.username} {self.status}"
