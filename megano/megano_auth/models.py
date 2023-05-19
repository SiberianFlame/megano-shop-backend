from django.contrib.auth.models import User
from django.db import models

def profile_avatar_directory_path(instance, filename):
    return 'avatar/{0}/{1}'.format(instance.user.username, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='user', related_name='profile')
    full_name = models.CharField(max_length=150, null=True, blank=True, verbose_name='full name')
    email = models.CharField(max_length=100, null=True, blank=True, verbose_name='email')
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='phone')
    avatar = models.ImageField(upload_to=profile_avatar_directory_path,
                               null=True,
                               blank=True,
                               verbose_name='avatar',
                               default='avatar/def.png')

    def __str__(self):
        return f'{self.user.username} profile'

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'