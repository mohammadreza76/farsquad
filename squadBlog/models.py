from django.db import models
from datetime import date
from .utils import unique_slug_generator
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from accounts.models import User
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150)
    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Post(models.Model):
    text = models.TextField(null=True)
    categories = models.ManyToManyField(Category)
    slug = models.SlugField(blank=True, null=True)

    def get_absolute_url(self):
        """Returns the url to access a detail record for this post."""
        return reverse('post-detail', args=[str(self.id)]) 

@receiver(post_save, sender=Post)
def generate_unique_slug_for_posts(sender, instance, created, *args, **kwargs):

    if created:
        instance.slug = unique_slug_generator(instance)
        instance.save()        

class Comment(models.Model):
    answer_body = models.TextField(null=True,help_text='لطفا جواب های خود را اینجا وارد کنید')   
    question_body = models.TextField(null=True,help_text='لطفا سوالات خود را اینجا وارد کنید')
    create_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post",on_delete=models.CASCADE,related_name='comments', related_query_name='comment') 
    owner = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
   
