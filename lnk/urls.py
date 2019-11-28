"""lnk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.views.static import serve
from lnk.settings import MEDIA_ROOT
import xadmin
from goods import views as good_view
from user import views as user_view
from user_operation import views as u_v
from trade import views as trade_cart
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_jwt.views import obtain_jwt_token
router = DefaultRouter()
router.register(r'goods',good_view.GoodViewSet,base_name='goods')
router.register(r'categorys',good_view.GoodsCategoryViewSet,base_name='categorys')
router.register(r'banner',good_view.BannerViewset,base_name='banner')
router.register(r'hotsearchs',good_view.HotSearchWordsViewSet,base_name='hotsearchs')
router.register(r'priceRange',good_view.GoodsRangeViewSet,base_name='priceRange')
router.register(r'code',user_view.MessageViewSet,base_name='code')
router.register(r'users',user_view.UserViewSet,base_name='users')
router.register(r'userfavs',u_v.UserFavViewSet,base_name='userfavs')
router.register(r'address',u_v.UserAddressViewSet,base_name='address')
router.register(r'messages',u_v.UserLeavingMessageViewSet,base_name='messages')
router.register(r'shopcarts',trade_cart.ShoppingCartViewSet,base_name='shopcarts')
router.register(r'orders',trade_cart.OrderViewset,base_name='orders')
router.register(r'indexgoods',good_view.IndexGoodsViewSet,base_name='indexgoods')

# router.register(r'users',user_view.UserInfoViewSet,base_name='users')
urlpatterns = [
    url('xadmin/', xadmin.site.urls),
    url('ueditor/', include('DjangoUeditor.urls')),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^api/',include(router.urls)),
    url(r'^api/login/',obtain_jwt_token),
    url(r'^api/delshopcarts/$',trade_cart.ShoppingCartViewSet.as_view({'delete': 'destroy'})),
    url(r'^alipay/return/',trade_cart.AlipayView.as_view())
]
