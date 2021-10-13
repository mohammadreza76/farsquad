from django.db import models
import uuid 
# Create your models here.

class Project(models.Model):
    name= models.CharField(max_length=90,null=True)
    description= models.TextField(null=True)
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)