from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView

from products.forms import CategoryForm, ProductForm
from products.models import Category, Product


class CategoryListView(ListView):
    model = Category
    template_name ='category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return super().get_queryset()


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_create.html'
    context_object_name = 'category_add'
    success_url = reverse_lazy('products:category_list')


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_update.html'
    context_object_name = 'category_update'
    success_url = reverse_lazy('products:category_list')


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'category_detail'



class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category_delete.html'
    context_object_name = 'category_delete'
    success_url = reverse_lazy('products:category_list')


class ProductListView(ListView):
    model = Product
    template_name ='product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return super().get_queryset()


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_create.html'
    context_object_name = 'product_add'
    success_url = reverse_lazy('products:product_list')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_update.html'
    context_object_name = 'product_update'
    success_url = reverse_lazy('products:product_list')


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_delete.html'
    context_object_name = 'product_delete'
    success_url = reverse_lazy('products:product_list')












