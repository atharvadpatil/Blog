from django.db import models


from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class BlogPost(models.Model):
    
    title = models.TextField()
    slug = models.SlugField(unique=True)
    content = models.TextField(null=True, blank=True)
 
    def get_absolute_url(self):
        return f"/blog_post/{self.slug}"

    def get_edit_url(self):
        return f"/blog_post/{self.slug}/edit/"

    def get_delete_url(self):
        return f"/blog_post/{self.slug}/delete/"

    def __str__(self):
        return self.slug

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

