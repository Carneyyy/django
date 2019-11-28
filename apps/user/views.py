from django.shortcuts import render
from user.serializers import MessageSerializer,UserRegisterSerializer,UserInfoSerislizer
from user.models import UserProfile,VerifyCode
from lnk.settings import APIKEY
from tools.yunpian import YunPian
from random import choice
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler,jwt_encode_handler
from rest_framework import status
# Create your views here.

class MessageViewSet(CreateModelMixin,GenericViewSet):
    queryset = VerifyCode.objects.all()
    serializer_class = MessageSerializer
    def get_code(self):
        # 生成验证码
        str = '1234567890'
        nums= []
        for i in range(0,4):
            num = choice(str)
            nums.append(num)
        return ''.join(nums)
    def create(self, request, *args, **kwargs):
        # post请求添加数据
        serializer = self.get_serializer(data=request.data)
        # 验证数据
        serializer.is_valid(raise_exception=True)
        # 生成验证码 并且发送
        mobile = serializer.validated_data['mobile']
        # 生成验证码
        code = self.get_code()
        # 发送验证码
        yp = YunPian(APIKEY)
        result = yp.send_message(code,mobile)
        print(result)
        print(type(result['code']))
        if result['code'] == 0:
            # 验证码发送成功
            # 保存数据
            verifycode = VerifyCode(code=code,mobile=mobile)
            verifycode.save()
            return Response({'code':1,'msg':result['msg'],'data':code},
                            status=status.HTTP_201_CREATED)
        else:
            # 验证码发送失败
            return Response({'code':0,'msg':result['msg']},
                            status=status.HTTP_400_BAD_REQUEST)
class UserViewSet(CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserRegisterSerializer

    def get_authenticators(self):
        if self.request.method == 'post':
            return []
        else:
            return [SessionAuthentication(), JSONWebTokenAuthentication()]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegisterSerializer
        return UserInfoSerislizer

    def get_object(self):
        return UserProfile.objects.filter(
            id=self.request.user.id
        ).first()
    # def get_permissions(self):
    #     if self.action == 'create':
    #         return []
    #     return ['权限对象']
    # def retrieve(self, request, *args, **kwargs):
    #     instance = UserProfile.objects.filter(id=request.user.id).first()
    #     ser = self.get_serializer(instance)
    #     return Response(ser.data)
    #
    #     # 注册并登录
    #
    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = UserProfile.objects.filter(id=request.user.id).first()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #
    #     if getattr(instance, '_prefetched_objects_cache', None):
    #         instance._prefetched_objects_cache = {}
    #
    #     return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # post请求添加数据
        serializer = self.get_serializer(data=request.data)
        # 验证数据
        serializer.is_valid(raise_exception=True)
        # 保存数据
        user = self.perform_create(serializer)
        # 注册完成后，执行登录
        re_dict = serializer.data
        # 生成token(
        # 参照的是urls.py文件中的
        # obtain_jwt_token->ObtainJSONWebToken->
        # JSONWebTokenSerializer->validate(self, attrs)
        # 方法生成token的方式
        # )
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)


    def perform_create(self, serializer):
        return serializer.save()
