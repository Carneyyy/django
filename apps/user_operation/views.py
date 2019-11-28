from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin,ListModelMixin,DestroyModelMixin
from rest_framework.viewsets import GenericViewSet,ModelViewSet
from .serializers import UserFavSerializer,UserDetailSerializer,UserAddressSerializer,UserLeavingMessageSerializer
from tools.permission import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import UserFav,UserAddress,UserLeavingMessage
# Create your views here.
class UserFavViewSet(CreateModelMixin,ListModelMixin,DestroyModelMixin,GenericViewSet):
    queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer
    authentication_classes = [SessionAuthentication,JSONWebTokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly,IsAuthenticated]
    lookup_field = 'goods_id'
    def get_serializer_class(self):
        if self.action == 'list':
            return UserDetailSerializer
        return UserFavSerializer
    def get_queryset(self):
        queryset = UserFav.objects.filter(user=self.request.user)
        return queryset


    def perform_create(self, serializer):
        instance = serializer.save()
        goods = instance.goods
        goods.fav_num += 1
        goods.save()

    def perform_destroy(self, instance):
        goods = instance.goods
        goods.fav_num -= 1
        goods.save()
        instance.delete()

class UserAddressViewSet(ModelViewSet):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
class UserLeavingMessageViewSet(ModelViewSet):
    queryset = UserLeavingMessage.objects.all()
    serializer_class = UserLeavingMessageSerializer
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

