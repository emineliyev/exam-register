from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Ad')
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Soyad')
    avatar = models.ImageField(upload_to="avatars/", default="avatars/default.jpg", verbose_name="Loqotip")

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создаем профиль при создании пользователя"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохраняем профиль при обновлении пользователя"""
    instance.profile.save()
