from django.db.models import Q
from django.views.generic import DetailView, ListView

from .models import Category, Product


class ProductListView(ListView):
    """Список активних товарів із пошуком, фільтрами та сортуванням."""

    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        queryset = (
            Product.objects
            .filter(is_active=True)
            .select_related("category", "brand")
        )

        search_query = self.request.GET.get("q", "").strip()
        category_slug = self.request.GET.get("category", "").strip()
        sort_by = self.request.GET.get("sort", "newest")

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
                | Q(description__icontains=search_query)
                | Q(brand__name__icontains=search_query)
                | Q(category__name__icontains=search_query)
            )

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        sort_options = {
            "newest": "-created_at",
            "price_asc": "price",
            "price_desc": "-price",
            "popular": "-popularity_score",
        }

        return queryset.order_by(
            sort_options.get(sort_by, "-created_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categories"] = Category.objects.filter(is_active=True)
        context["search_query"] = self.request.GET.get("q", "")
        context["selected_category"] = self.request.GET.get("category", "")
        context["selected_sort"] = self.request.GET.get("sort", "newest")

        return context


class ProductDetailView(DetailView):
    """Сторінка окремого товару."""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.filter(
            is_active=True,
        ).select_related("category", "brand")
# Create your views here.
