from django.views import generic

from product.models import Variant, Product,ProductVariant, ProductVariantPrice
from django.db.models import F, Q
from datetime import datetime

class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.all().values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context


def save_product(request, product):
    if request.method == "POST":
        prod = Product(title=product["title"], sku=product["sku"], description=product["description"], created_at=datetime.now())
        prod.save()
        # save others as well


class UpdateProduct(generic.UpdateView):
    model = Product
    template_name = 'products/update_product.html'
    fields = [
        "title",
        "description"
    ]
    success_url = "/"


class ProductListView(generic.ListView):
    template_name = 'products/list.html'
    paginate_by = 2
    model = Product
    totals = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['totals'] = self.totals
        context['variant1'] = ProductVariant.objects.filter(variant_id=1).values('variant_id', name=F('variant_title')).distinct()
        context['variant2'] = ProductVariant.objects.filter(variant_id=2).values('variant_id', name=F('variant_title')).distinct()
        context['variant3'] = ProductVariant.objects.filter(variant_id=3).values('variant_id', name=F('variant_title')).distinct()
        return context

    def get_queryset(self):
        queryset = Product.objects.all()
        print("VAR: ", self.request.GET.get("variant", 0))
        if self.request.GET.get('title', ""):
            queryset = queryset.filter(title__contains=self.request.GET["title"])
        if self.request.GET.get("variant", 0):
            products = [i['product_id'] for i in ProductVariant.objects.filter(variant_id=self.request.GET.get("variant", 0)).values('product_id')]
            queryset = queryset.filter(id__in=products)
        if self.request.GET.get('price_from', 0):
            variants = ProductVariantPrice.objects.filter(price__gte=self.request.GET.get('price_from', 0)).values(
                idd=F('product_variant_one__product_id'))
            variants |= ProductVariantPrice.objects.filter(price__gte=self.request.GET.get('price_from', 0)).values(
                idd=F('product_variant_two__product_id'))
            variants |= ProductVariantPrice.objects.filter(price__gte=self.request.GET.get('price_from', 0)).values(
                idd=F('product_variant_three__product_id'))
            products = [i['idd'] for i in variants]
            queryset = queryset.filter(id__in=products)
        if self.request.GET.get('price_to', 0):
            variants = ProductVariantPrice.objects.filter(price__lte=self.request.GET.get('price_to', 0)).values(
                idd=F('product_variant_one__product_id'))
            variants |= ProductVariantPrice.objects.filter(price__lte=self.request.GET.get('price_to', 0)).values(
                idd=F('product_variant_two__product_id'))
            variants |= ProductVariantPrice.objects.filter(price__lte=self.request.GET.get('price_to', 0)).values(
                idd=F('product_variant_three__product_id'))
            products = [i['idd'] for i in variants]
            queryset = queryset.filter(id__in=products)
        if self.request.GET.get('date', 0):
            queryset = queryset.filter(created_at=self.request.GET.get('date', 0))
        self.totals = queryset.count()
        return queryset.order_by('created_at')