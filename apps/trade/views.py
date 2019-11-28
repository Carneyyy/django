from django.shortcuts import render
from rest_framework.mixins import ListModelMixin,CreateModelMixin,DestroyModelMixin,\
    UpdateModelMixin,RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet,ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from tools.permission import IsOwnerOrReadOnly
from .models import ShoppingCart,OrderInfo,OrderGoods
from .serializer import ShoppingCartSerializer,ShoppingCartDetailSerializer,OrderSerializer
# Create your views here.

class ShoppingCartViewSet(ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    lookup_field = 'goods_id'

    permission_classes = [
        IsAuthenticated,
        IsOwnerOrReadOnly,
    ]
    authentication_classes = [
        SessionAuthentication,
        JSONWebTokenAuthentication,
    ]
    def get_serializer_class(self):
        if self.action == 'list':
            return ShoppingCartDetailSerializer
        return ShoppingCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(
            user=self.request.user.id
        )
    def destroy(self, request, *args, **kwargs):
        goods_id = kwargs.get('goods_id')
        if goods_id:
            return super(ShoppingCartViewSet, self).destroy(request,*args,**kwargs)
        else:
            queryset = self.get_queryset()
            for i in queryset:
                self.perform_destroy(i)
            return Response(status=status.HTTP_204_NO_CONTENT)

class OrderViewset(ListModelMixin,CreateModelMixin,DestroyModelMixin,RetrieveModelMixin,GenericViewSet):
    # 权限设置
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    # 认证设置
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    serializer_class = OrderSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.save()
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart  in shop_carts:
            #获取购物车中的所有商品信息保存在订单商品中
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()
            shop_cart.delete()
        # return order
from rest_framework.views import APIView
from tools.alipay import AliPay
from lnk.settings import APPID,PUBLIC_KEY, PRIVATE_KEY,TEXT_URL
from rest_framework.response import Response
from datetime import datetime
from django.shortcuts import redirect

class AlipayView(APIView):
    def get(self, request):
        """
        处理支付宝的return_url返回
        :param request:
        :return:
        """
        processed_dict = {}
        for key, value in request.GET.items():
            processed_dict[key] = value

        sign = processed_dict.pop("sign", None)

        print('======',processed_dict)

        alipay = AliPay(
            appid=APPID,
            app_notify_url="http://127.0.0.1:8000/alipay/return/",
            app_private_key_path=PRIVATE_KEY,
            alipay_public_key_path=PUBLIC_KEY,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://127.0.0.1:8000/alipay/return/"
        )
        #根据成功返回的参数和签名是否一致
        verify_re = alipay.verify(processed_dict, sign)

        if verify_re is True:
            #获取订单号
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', 'TRADE_SUCCESS')
            #更新订单支付信息
            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            response = redirect("http://127.0.0.1:8080/#/app/home/index")
            response.set_cookie("nextPath","pay", max_age=3)
            return response
        else:
            response = redirect("http://127.0.0.1:8080/#/app/home/index")
            return response

    def post(self, request):
        """
        处理支付宝的notify_url
        :param request:
        :return:
        """
        processed_dict = {}
        for key, value in request.POST.items():
            processed_dict[key] = value

        sign = processed_dict.pop("sign", None)

        alipay = AliPay(
            appid=APPID,
            app_notify_url="http://127.0.0.1:8000/alipay/return/",
            app_private_key_path=PRIVATE_KEY,
            alipay_public_key_path=PUBLIC_KEY,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://127.0.0.1:8000/alipay/return/"
        )

        verify_re = alipay.verify(processed_dict, sign)

        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', 'TRADE_SUCCESS')

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                order_goods = existed_order.goods.all()
                for order_good in order_goods:
                    goods = order_good.goods
                    goods.sold_num += order_good.goods_num
                    goods.save()

                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            return Response("success")
