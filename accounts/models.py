from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.dispatch import receiver #phase2
from django.db.models.signals import post_save #phase2
from django.utils.translation import gettext_lazy as _ #phase2
from .utils import unique_slug_generator #phase2.1

def upload_to(instance, filename):
    #phase2
    return 'profiles/{filename}'.format(filename=filename)


class UserManager(BaseUserManager):
    # add name in parameters of create_user for phase2
    def create_user(self, phone, password=None, name=None,is_staff=False, is_active=True, is_admin=False):
        if not phone:
            raise ValueError('users must have a phone number')
        if not password:
            raise ValueError('user must have a password')

        user_obj = self.model(
            phone=phone,
            name=name #phase2
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, phone, password=None,name=None):
        user = self.create_user(
            phone,
            password=password,
            is_staff=True,
            name=name,


        )
        return user

    def create_superuser(self, phone, password=None,name=None):
        user = self.create_user(
            phone,
            password=password,
            is_staff=True,
            is_admin=True,
            name=name

        )
        return user


class User(AbstractBaseUser):
    phone_regex = RegexValidator( regex   =r'^\+?1?\d{9,14}$', message ="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    phone       = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    name        = models.CharField(max_length = 20, blank = True, null = True)
    standard    = models.CharField(max_length = 3, blank = True, null = True)
    mohavereh_score       = models.IntegerField(default = 0) #phase2.5
    squad_score       = models.IntegerField(default = 0)#phase2.5
    overall_score       = models.IntegerField(default = 0)#phase2.5
    first_login = models.BooleanField(default=False)
    active      = models.BooleanField(default=True)
    staff       = models.BooleanField(default=False)
    admin       = models.BooleanField(default=False)
    timestamp   = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True, null=True)
    help_text = "fgkldm"
    'add slug in in this class and help_text' 'phase2.1'
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone

    def get_full_name(self):
        return self.name #phase2

    def get_short_name(self):
        return self.name #phase2

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):

        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

@receiver(post_save, sender=User) #phase2.1
def generate_unique_slug_for_posts(sender, instance, created, *args, **kwargs):

    if created:
        instance.slug = unique_slug_generator(instance)
        instance.save()         
            
class PhoneOTP(models.Model):
    phone_regex = RegexValidator( regex   =r'^\+?1?\d{9,14}$', message ="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    phone       = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    otp         = models.CharField(max_length = 9, blank = True, null= True)
    count       = models.IntegerField(default = 0, help_text = 'Number of otp sent')
    logged      = models.BooleanField(default = False, help_text = 'If otp verification got successful')
    forgot      = models.BooleanField(default = False, help_text = 'only true for forgot password')
    forgot_logged = models.BooleanField(default = False, help_text = 'Only true if validdate otp forgot get successful')


    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)

class Profile(models.Model):
    
    #Represents a "user profile" inside out system. Stores all user account
    #related data, such as 'email address' and 'name'.
     
    'new_phase2'
    'add slug in in this class' 'phase2.1'
    GENDER = (
        ('مرد', 'م'),
        ('زن', 'ز'),
    )
    user = models.ForeignKey('User',on_delete=models.CASCADE)
    gender = models.CharField(max_length=6, choices=GENDER,blank=True)
    date_of_birth = models.DateField(blank=True,null=True)
    major = models.CharField(max_length=30,blank=True)
    education_degree = models.CharField(max_length=20,blank=True)
    image = models.ImageField(
        _("Image"), upload_to=upload_to,blank=True,null=True)
    phone_regex = RegexValidator( regex   =r'^\+?1?\d{9,14}$', message ="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    phone       = models.CharField(validators=[phone_regex], max_length=17, unique=True,blank=True) 
    email = models.EmailField(max_length=60,blank=True)  
    slug = models.SlugField(blank=True) #phase2.1
    name=models.CharField(max_length=90,blank=True)
 
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance,phone=instance.phone,slug=instance.slug,name=instance.name) #phase2.1 for slug
          