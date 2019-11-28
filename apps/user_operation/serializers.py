from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import UserFav,Goods,UserAddress,UserLeavingMessage
from goods.serializers import GoodSerializers

class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # goods = serializers.SerializerMethodField()
    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=['user','goods'],
                message='该商品已收藏'
            )
        ]
        model = UserFav
        fields = ['user','goods','id']
    # def get_goods(self, row):
    #     good_id = row.goods.id
    #     queryset = Goods.objects.filter(id=good_id).first()
    #     ser = GoodSerializers(instance=queryset, many=False)
    #     return ser.data
class UserDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    goods = serializers.SerializerMethodField()

    def get_goods(self, row):
        good_id = row.goods.id
        queryset = Goods.objects.filter(id=good_id).first()
        ser = GoodSerializers(instance=queryset, many=False)
        return ser.data

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=['user', 'goods'],
                message='该商品已收藏'
            )
        ]
        model = UserFav
        fields = ['user', 'goods', 'id']


class UserAddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = UserAddress
        fields = '__all__'
class UserLeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = UserLeavingMessage
        fields = '__all__'