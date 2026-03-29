from django.forms import ModelForm

from products.models import Category, Product


class CategoryForm(ModelForm):
    """ Форма Создания Категории"""
    class Meta:
        model = Category
        fields = ['name', 'photo', 'description']

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите название категории'})
        self.fields['photo'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Фото'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Описание'})



class ProductForm(ModelForm):
    """ Форма Создания Продукта"""
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите название товара'})
        self.fields['photo'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Фото'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Описание товара'})
        self.fields['category'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Категория товара'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Количество товара'})




