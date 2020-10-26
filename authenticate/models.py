from django.db import models
from django.contrib import admin
from django.contrib.auth.models import (
     AbstractBaseUser
)
# class UserProfile(models.Model):
#     user = models.OneToOneField(User)
#     user_id = models.CharField(max_length=200)
#     email = models.EmailField(verbose_name='email address', max_length=255, unique=True, db_index=True,)
#     first_name = models.CharField(max_length=200)
#     last_name = models.CharField(max_length=200)
# 
#     def __unicode__(self):
#         return unicode(self.user_id)

class users(AbstractBaseUser):

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        db_index=True,
    )
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    
#     class Meta:
#         app_label = 'components'