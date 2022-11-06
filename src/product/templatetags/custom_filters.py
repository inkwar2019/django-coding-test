from django import template
from product.models import Product, ProductVariant, ProductVariantPrice
from django.db.models import F, Q

register = template.Library()


def min_id(value): # Only one argument.
    """Converts a string into all lowercase"""
    ids = [i.id for i in value]
    return min(ids)


def max_id(value): # Only one argument.
    """Converts a string into all lowercase"""
    ids = [i.id for i in value]
    return max(ids)


def get_variants(product):
    variants = ProductVariantPrice.objects.filter(product_variant_one__product_id=product.id).values(v=F('product_variant_one__variant_title'),
                                                                           p=F('price'),
                                                                           s=F('stock'))
    variants |= ProductVariantPrice.objects.filter(product_variant_two__product_id=product.id).values(
                                                                            v=F('product_variant_two__variant_title'),
                                                                            p=F('price'),
                                                                            s=F('stock'))
    variants |= ProductVariantPrice.objects.filter(product_variant_three__product_id=product.id).values(
                                                                            v=F('product_variant_three__variant_title'),
                                                                            p=F('price'),
                                                                            s=F('stock'))
    return variants


@register.simple_tag(name='total_product')
def total_product():
    return Product.objects.all().count()


@register.simple_tag(name='total_variant')
def total_variant():
    return ProductVariant.objects.all().values(id=F('id'), name=F('variant_title'))


#filters
register.filter('min_id', min_id)
register.filter('max_id', max_id)
register.filter('get_variants', get_variants)


