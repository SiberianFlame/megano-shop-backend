from django.contrib.auth.models import User
from django.db import models

def profile_avatar_directory_path(instance: 'Profile', filename):
    """
    Creating path for profile avatar image
    :param instance: Profile object
    :param filename: Name of the file
    :return: Path string
    """

    return 'avatar/{0}/{1}'.format(instance.user.username, filename)

class Profile(models.Model):
    """
    Profile model to extend standard User model
    """

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