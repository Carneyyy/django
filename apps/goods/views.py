from django.shortcuts import render
from rest_framework.mixins import ListModelMixin,RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from .serializers import GoodSerializers,GoodsCategorySerializers,BannerSerializer,\
    HotsSearchWordKeySerializer,GoodsPriceRangeSerializer,IndexAdCategorySerializer
from .models import Goods,GoodsCategory,Banner,HotSearchWords,GoodsPriceRange
from .filter import GoodsFilter
from django_filters.rest_framework import DjangoFilterBackend
#     rest_framework 内部过滤器
from rest_framework import filters
from tools.pagination import MyPageNumberPagination
# Create your views here.


#商品列表
class GoodViewSet(ListModelMixin,RetrieveModelMixin,GenericViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodSerializers
    pagination_class = MyPageNumberPagination
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter]
    filter_class = GoodsFilter
    ordering_fields=['sold_num','shop_price']
    search_fields = ['name','goods_brief','goods_desc']
class GoodsCategoryViewSet(ListModelMixin,RetrieveModelMixin,GenericViewSet):
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = GoodsCategorySerializers
class BannerViewset(ListModelMixin,GenericViewSet):
    queryset = Banner.objects.all().order_by('index')
    serializer_class = BannerSerializer

class HotSearchWordsViewSet(ListModelMixin,GenericViewSet):
    queryset = HotSearchWords.objects.all().order_by('index')
    serializer_class = HotsSearchWordKeySerializer

class GoodsRangeViewSet(ListModelMixin,GenericViewSet):
    queryset = GoodsPriceRange.objects.all()
    serializer_class = GoodsPriceRangeSerializer


class IndexGoodsViewSet(ListModelMixin,GenericViewSet):
    """首页底部分类信息视图"""
    queryset = GoodsCategory.objects.all()
    serializer_class = IndexAdCategorySerializer

    def get_queryset(self):
        return GoodsCategory.objects.filter(
            is_tab=True,name__in = ['奶类食品']
        )

