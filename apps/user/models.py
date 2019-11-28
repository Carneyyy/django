from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
# Create your models here.


class UserProfile(AbstractUser):
    GENDER = (
        ('male', '男'),
        ('female','女')
    )
    name = models.CharField(max_length=30,null=True,blank=True,verbose_name='用户名')
    birthday = models.DateField(default=datetime.now,null=True,blank=True,verbose_name='出生年月')
    gender = models.CharField(choices=GENDER,default='male',null=True,blank=True,verbose_name='性别',max_length=6)
    email = models.EmailField(max_length=60,null=True,blank=True,verbose_name='邮箱')
    mobile = models.CharField(max_length=11,null=False,blank=False,verbose_name='手机号')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

class VerifyCode(models.Model):
    code = models.CharField(max_length=4,null=False,blank=False,verbose_name='验证码')
    mobile = models.CharField(max_length=11,verbose_name='手机号')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='创建时间')
    class Meta:
        verbose_name = '验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code