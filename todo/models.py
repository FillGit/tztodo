from django.db import models

# Create your models here.
from django.db import models

from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class CompanyName(models.Model):
    name = models.CharField(max_length=50, help_text="RGD, Aeroflot, Rosneft, Gazprom or empty")
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enabled_company = models.ManyToManyField('CompanyName', blank=True, related_name="companies", help_text="access to company data")
    date_idsession = models.DateField(null=True, blank=True)
    idsession = models.CharField(max_length=50, blank=True)
    active_company = models.CharField(max_length=50, blank=True)
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)



class Desks(models.Model):
    
    company_name = models.ForeignKey('CompanyName', on_delete=models.CASCADE) 
    created = models.DateTimeField(auto_now_add=True)
    done = models.BooleanField(default=False)
    due_date = models.DateField()
    task = models.TextField()
    
    executor = models.CharField(max_length=50, null=True, blank=True, help_text="User executor")
    owner = models.ForeignKey('auth.User', related_name='desks', on_delete=models.CASCADE)
    
    class Meta:
        ordering = ('created',)

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        super(Desks, self).save(*args, **kwargs)

