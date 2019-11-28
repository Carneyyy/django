import django_filters
from .models import Goods
from django.db.models import Q

class GoodsFilter(django_filters.rest_framework.FilterSet):
    # 商品过滤 根据价格区间
    pricemin = django_filters.NumberFilter(
        field_name='shop_price',
        help_text='最低价格',
        lookup_expr='gte',  #gte大于等于
    )
    pricemax = django_filters.NumberFilter(
        field_name='shop_price',
        help_text='最高价格',
        lookup_expr='lte',  # gte大于等于
    )

    top_category = django_filters.NumberFilter(
        method='top_category_filter'
    )

    def top_category_filter(self,queryset,name,value):
        #     value 指的是分类id
        return queryset.filter(
            Q(category_id=value)|
            Q(category__parent_category_id=value)|
            Q(category__parent_category__parent_category_id=value)
        )
    class Meta:
        model = Goods
        fields = ['pricemin','pricemax','is_hot','is_new']
