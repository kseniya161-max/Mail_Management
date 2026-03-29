from django.urls import path

from products.views import CategoryCreateView, CategoryListView, CategoryUpdateView, CategoryDetailView, CategoryDeleteView, ProductListView, ProductUpdateView, ProductCreateView, ProductDeleteView

app_name = "products"

urlpatterns = [
    path('', CategoryListView.as_view(), name='category_list'),
    path('category/add/', CategoryCreateView.as_view(), name='category_add'),
    path('category/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_edit'),
    path('category/<int:pk>/detail/', CategoryDetailView.as_view(), name='category_detail'),
    path('category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    path('products/all/', ProductListView.as_view(), name='product_list'),
    path('products/add/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),]
