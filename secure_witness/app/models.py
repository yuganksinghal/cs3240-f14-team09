from django.db import models
from django.contrib.auth.models import User

class Bulletin(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey(User)
    anonymous = models.BooleanField(default=False)

    def __str__(self):
        return self.title
        
class File(models.Model):
    filename = models.CharField(max_length=50)
    path = models.FileField(upload_to='Bulletins/user/%Y/%m/%d')
    bulletin = models.ForeignKey(Bulletin)
    users = models.ManyToManyField(User)
    
    def __str__(self):
        return self.filename
        
