from django.contrib.auth import get_user_model
import pytest

from documents.services.file_service import generate_offer_file, generate_offer_excel
from products.models import Product, Category

User = get_user_model()


@pytest.mark.django_db
def test_generate_offer_file():
    user = User.objects.create(username="test_user")
    product = Product.objects.create(
        name="test_product",
        category=Category.objects.create(name="test_category"),
        quantity=10,
    )

    qs = Product.objects.filter(id=product.id)
    offer_file = generate_offer_file(user, qs)
    generate_offer_excel(offer_file)

    assert offer_file is not None
    assert offer_file.name.startswith("offer_")
    assert offer_file.file is not None
    assert offer_file.file.name.endswith(".xlsx")
    assert offer_file.products.count() == 1
    assert offer_file.created_by == user
