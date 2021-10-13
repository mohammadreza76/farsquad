from django.db import models
from .utils import unique_slug_generator
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User 
# Create your models here.
class InformalText(models.Model):
    text = models.TextField(null=True)
    slug = models.SlugField(blank=True, null=True)
    helper_t = "oijn"
    has_answer = models.CharField(default='no',max_length=20) 
    validate_answer = models.CharField(default='no',max_length=20)#phase2.5
    blocked_by_person_for_answering = models.BooleanField(default=False)#phase2.6
    blocked_by_person_for_validating = models.BooleanField(default=False)#phase2.6
    start_time=models.DateTimeField(null=True,auto_now=True)#phase3.4
    still_blocked=models.BooleanField(default=False)#phase3.4

    def get_absolute_url(self):
        """Returns the url to access a detail record for this MohaverehText."""
        return reverse('MohaverehText-detail', args=[str(self.id)]) 

@receiver(post_save, sender=InformalText)
def generate_unique_slug_for_posts(sender, instance, created, *args, **kwargs):

    if created:
        instance.slug = unique_slug_generator(instance)
        instance.save()  

class FormalText(models.Model):
    answer_body = models.TextField(null=True)   
    create_on = models.DateTimeField(auto_now_add=True,null=True)
    informalـtext = models.OneToOneField("InformalText",on_delete=models.CASCADE,related_name='formalTexts', related_query_name='formalText',
                   null=True) 
    owner = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
           