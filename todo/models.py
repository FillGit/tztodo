from django.db import models

# Create your models here.
from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())

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
    
    executor = models.CharField(max_length=50, blank=True, default='', help_text="User executor")
    owner = models.ForeignKey('auth.User', related_name='desks', on_delete=models.CASCADE)
    
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    title = models.CharField(max_length=100, blank=True, default='')
    linenos = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('created',)

from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

def save(self, *args, **kwargs):
    """
    Use the `pygments` library to create a highlighted HTML
    representation of the code snippet.
    """
    lexer = get_lexer_by_name(self.language)
    linenos = 'table' if self.linenos else False
    options = {'title': self.title} if self.title else {}
    formatter = HtmlFormatter(style=self.style, linenos=linenos,
                              full=True, **options)
    self.highlighted = highlight(self.code, lexer, formatter)
    super(Desks, self).save(*args, **kwargs)
