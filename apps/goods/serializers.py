from rest_framework import serializers
from .models import Goods,GoodsCategory,Banner,HotSearchWords,GoodsPriceRange,GoodsImage,GoodsCategoryBrand,IndexAd
from django.db.models import Q
class GoodsSerializers(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M'
    )
    class Meta:
        model = Goods
        fields = '__all__'
class GoodsCategorySerializer3(serializers.ModelSerializer):
    # 三级分类序列化
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsCategorySerializer2(serializers.ModelSerializer):
    # 二级分类序列化
    sub_cat = GoodsCategorySerializer3(many=True)
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsCategorySerializers(serializers.ModelSerializer):
    # 一级分类序列化
    sub_cat = GoodsCategorySerializer2(many=True)
    class Meta:
        model = GoodsCategory
        fields = '__all__'

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class HotsSearchWordKeySerializer(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M:%S'
    )
    class Meta:
        model = HotSearchWords
        fields = '__all__'
class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ['image']

class GoodSerializers(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M'
    )
    images = GoodsImageSerializer(many=True)
    class Meta:
        model = Goods
        fields = '__all__'


class GoodsPriceRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsPriceRange
        fields = '__all__'


#分类下的商家品牌广告序列化
class GoodsCategoryBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = '__all__'



class IndexAdCategorySerializer(serializers.ModelSerializer):
    brands = GoodsCategoryBrandSerializer(many=True)
    #分类下的商品
    goods = serializers.SerializerMethodField()
    #获取当前分类下的二级分类
    sub_cat = GoodsCategorySerializer2(many=True)
    #获取当前分类下的商品广告
    ad_goods = serializers.SerializerMethodField()

    def get_goods(self,row):
        #row指的是GoodsCategory
        all_goods = Goods.objects.filter(
            Q(category_id=row.id) |
            Q(category__parent_category_id=row.id) |
            Q(category__parent_category__parent_category_id=row.id)

        )
        ser = GoodsSerializers(instance=all_goods,many=True,context={'request':self.context['request']})
        return ser.data

    def get_ad_goods(self,row):
        # 获取当前分类下的商品广告
        print(row.id)
        ad_goods = IndexAd.objects.filter(category=row.id).first()
        print(ad_goods)
        goods = ad_goods.goods
        obj = Goods.objects.filter(id=goods.id).first()

        ser = GoodsSerializers(instance=obj,many=False, context={'request':self.context['request']})
        return ser.data

    class Meta:
        model = GoodsCategory
        fields = '__all__'

