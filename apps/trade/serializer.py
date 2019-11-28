from rest_framework import serializers
from .models import ShoppingCart,OrderInfo,OrderGoods
from goods.models import Goods
import random,time
from goods.serializers import GoodSerializers
from tools.alipay import AliPay
from lnk.settings import APPID,PRIVATE_KEY,PUBLIC_KEY,TEXT_URL

class ShoppingCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(
        required=True,min_value=1,
        error_messages={
            'required':'请选择购买数量',
            'min_value':'购买数量必需大于0件'
        }
    )
    goods = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=Goods.objects.all()
    )
    def create(self, validated_data):
        user =self.context['request'].user
        goods = validated_data['goods']
        obj = ShoppingCart.objects.filter(
            user=user,
            goods=goods
        ).first()
        if obj:
            obj.nums += validated_data['nums']
            obj.save()
        else:
            obj = ShoppingCart.objects.create(**validated_data)
        return obj

    def update(self, instance, validated_data):
        nums = validated_data['nums']
        instance.nums = nums
        instance.save()
        return instance
    # class Meta:
    #     model = ShoppingCart
    #     fields = ['user','goods','nums']
class ShoppingCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodSerializers(many=False,read_only=True)
    # def get_goods(self,row):
    #     goods_id = row.goods.id
    #     obj = Goods.objects.filter(id=goods_id).first()
    #     ser = GoodSerializers(instance=obj,many=False)
    #     return ser.data
    class Meta:
        model = ShoppingCart
        fields = ['goods','nums']

class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodSerializers(many=False)
    class Meta:
        model = OrderGoods
        fields = '__all__'
class OrderSerializer(serializers.ModelSerializer):
    #隐藏用户信息
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    #订单状态用户不可修改提交，支付之后才可以修改
    pay_status = serializers.CharField(
        read_only=True
    )
    trade_no = serializers.CharField(
        read_only=True
    )
    order_sn = serializers.CharField(
        read_only=True
    )
    add_time = serializers.DateTimeField(
        read_only=True,
        format="%Y-%m-%d %H:%M"
    )
    pay_time = serializers.DateTimeField(
        read_only=True,
        format="%Y-%m-%d %H:%M"
    )
    goods = OrderGoodsSerializer(many=True,read_only=True)

    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self,row):
        #通过方法生成支付url地址
        alipay = AliPay(
            appid=APPID,
            app_notify_url="http://projectsedus.com/",
            app_private_key_path=PRIVATE_KEY,
            alipay_public_key_path=PUBLIC_KEY,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://127.0.0.1:8000/alipay/return/"
        )

        url = alipay.direct_pay(
            subject="测试订单",
            out_trade_no=row.order_sn,
            total_amount=row.order_mount
        )
        pay_url = "{url}?{data}".format(url=TEXT_URL,data=url)
        print(pay_url)
        return pay_url
    def get_order_sn_nums(self):
        # 唯一：当前时间+随机数字+用户id
        order_sn = "{time_str}{userid}{ranstr}".format(
            time_str=time.strftime("%Y%m%d%H%M%S"),
            userid=self.context['request'].user.id,
            ranstr=random.randint(10, 99)
        )

        return order_sn

    def validate(self, attrs):
        attrs['order_sn'] = self.get_order_sn_nums()
        return attrs
    class Meta:
        model = OrderInfo
        fields = ['user','post_script','address','signer_name',
                  'singer_mobile','order_mount','order_sn','trade_no',
                  'pay_status','pay_time','add_time','id','goods','alipay_url']