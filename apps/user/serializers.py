from rest_framework import serializers
from lnk.settings import REGEX_MOBILE
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from user.models import VerifyCode,UserProfile
from datetime import timedelta,datetime
import re
User = get_user_model()

class MessageSerializer(serializers.Serializer):
    mobile =serializers.CharField(max_length=11)
    def validate_mobile(self, value):
        obj = User.objects.filter(mobile=value)
        if obj:
            raise ValidationError('该用户已存在')
        if not re.match(REGEX_MOBILE,value):
            raise ValidationError('该手机号不合法')
        # VerifyCode.objects.filter(mobile=value).order_by('-add_time')
        noe_minutes_ago = datetime.now() - timedelta(hours=0,minutes=1,seconds=0)
        if VerifyCode.objects.filter(add_time__gte=noe_minutes_ago,mobile=value).count():
            raise ValidationError('距离上次发送验证码未超过60秒')

        return value

# 用户注册序列化
# 1,判断当前用户是否存在
# 2，判断验证码是否有效

class UserRegisterSerializer(serializers.Serializer):
    code = serializers.CharField(
        required=True,
        write_only=True,
        max_length=4,
        min_length=4,
        error_messages={
            'required':'请输入验证码',
            'blank': '请输入验证码',
            'max_length':'验证码格式错误',
            'min_length':'验证码格式错误'
        },
        help_text='验证码'
    )
    username = serializers.CharField(
        required=True,
        allow_blank=True,
        validators=[
            UniqueValidator(queryset=User.objects.all(),
                            message='用户已存在'
            )
        ],
        help_text='用户名'
    )
    password = serializers.CharField(
        style={'input_type': 'password'},
        required=True,
        write_only=True,
        help_text='密码'
    )
    def validate_code(self,value):
        # 查询是否发送验证码
        # username是手机号
        code_queryset = VerifyCode.objects.filter(
            mobile=self.initial_data['username']
        ).order_by('-add_time')
        if code_queryset:
            # 判断验证码是否有效
            last_code = code_queryset[0]
            five_minuter_ago = datetime.now()-timedelta(hours=0,minutes=5,seconds=0)
            if last_code.add_time > five_minuter_ago:
                #验证码没有过期 比对验证码是否一致
                if last_code.code != value:
                    raise ValidationError('验证码无效')
                else:
                    return value
            else:
                raise ValidationError('验证码已过期')
        else:
            raise ValidationError('无效验证码')
    def validate(self, attrs):
        # 验证attrs里存放的是序列化验证后的数据
        del attrs['code']
        attrs['mobile'] = attrs['username']
        return attrs
    def create(self, validated_data):
        instance = User.objects.create(**validated_data)
        # instance = super(UserRegisterSerializer, self).create(validated_data=validated_data)
        # instance.set_password(validated_data["password"])
        # instance.save()
        return instance

class UserInfoSerislizer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields = ['name','birthday','gender','mobile','email','id']