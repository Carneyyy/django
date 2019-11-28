from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

# pre_init                        # Django中的model对象执行其构造方法前,自动触发
# post_init                       # Django中的model对象执行其构造方法后,自动触发
# pre_save                        # Django中的model对象保存前,自动触发
# post_save                       # Django中的model对象保存后,自动触发
# pre_delete                      # Django中的model对象删除前,自动触发
# post_delete                     # Django中的model对象删除后,自动触发

User = get_user_model()

@receiver(post_save, sender=User)
def create_user(sender, instance=None, created=False, **kwargs):
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()