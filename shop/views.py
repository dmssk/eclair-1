from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from .models import Product as ProductModel


class Index(TemplateView):
    template_name = "shop/index/index.html"


class Product(TemplateView):
    template_name = "shop/product.html"

    def get_context_data(self, **kwargs):
        data = super(Product, self).get_context_data(**kwargs)
        article = data["article"]
        product = get_object_or_404(
            ProductModel.objects.prefetch_related("images"), article=article.upper()
        )
        data["product"] = product
        return data


class Cabinet(TemplateView):
    template_name = "shop/cabinet.html"


class About(TemplateView):
    template_name = "shop/about.html"


class CakeOrder(TemplateView):
    template_name = "shop/cake-order.html"


class Contacts(TemplateView):
    template_name = "shop/contacts.html"


class News(TemplateView):
    template_name = "shop/news.html"


class NewsItem(TemplateView):
    template_name = "shop/news-item.html"


class Cart(TemplateView):
    template_name = "shop/cart.html"


class Checkout(TemplateView):
    template_name = "shop/checkout.html"


class Review(TemplateView):
    template_name = "shop/review.html"


class Vacancies(TemplateView):
    template_name = "shop/vacancies.html"


def not_found(request, exception=None):
    return render(request, "shop/404.html", status=404)
