from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'user'
    verbose_name = "用户管理"
    def ready(self):
        import user.signal