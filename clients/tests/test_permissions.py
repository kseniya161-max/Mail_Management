import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from clients.models import Clients
from django.test import Client

User = get_user_model()


@pytest.mark.django_db
def test_client_list_visibility():
    user1 = User.objects.create_user(
        username="user1", password="pass", email="user@test.ru", role="user"
    )
    user2 = User.objects.create_user(
        username="user2", password="pass", email="user@test2.ru", role="user"
    )
    manager = User.objects.create_user(
        username="manager1", password="pass", email="manager@test1.ru", role="manager"
    )

    client_user1 = Clients.objects.create(
        user=user1, name="Client A", email="a@test.com", phone_number="+79123456789"
    )
    client_user2 = Clients.objects.create(
        user=user2, name="Client B", email="a@test2.com", phone_number="+79133456789"
    )
    client_manager = Clients.objects.create(
        user=manager,
        name="Manager's Client",
        email="mgr@test.com",
        phone_number="+79135556789",
    )

    client = Client()

    # Логиним user1
    client.force_login(user1)
    response = client.get(reverse("clients:client_list"))
    assert response.status_code == 200
    assert "list_clients" in response.context
    assert client_user1 in response.context["list_clients"]
    assert client_user2 not in response.context["list_clients"]
    assert client_manager not in response.context["list_clients"]

    # Логиним менеджера
    client.force_login(manager)
    response = client.get(reverse("clients:client_list"))
    assert client_manager in response.context["list_clients"]
    assert client_user1 not in response.context["list_clients"]
    assert client_user2 not in response.context["list_clients"]
