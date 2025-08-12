import pytest
from django.utils.timezone import now
from rest_framework.test import APIClient
from restaurants.models import Restaurant, Menu
from votes.models import Vote


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def register_user(api_client):
    def do_register(email="test@example.com", username="testuser", password="Testpass123"):
        response = api_client.post("/api/auth/register/", {
            "email": email,
            "username": username,
            "password": password
        }, format="json")
        return response
    return do_register


@pytest.fixture
def login_user(api_client, register_user):
    def do_login(email="test@example.com", password="Testpass123"):
        register_user(email=email, username="testuser", password=password)
        response = api_client.post("/api/auth/login/", {
            "email": email,
            "password": password
        }, format="json")
        tokens = response.json()
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        return tokens
    return do_login


# --------------------
# AUTH TESTS
# --------------------
@pytest.mark.django_db
def test_register_and_login(api_client, register_user):
    register_resp = register_user()
    assert register_resp.status_code == 201

    login_resp = api_client.post("/api/auth/login/", {
        "email": "test@example.com",
        "password": "Testpass123"
    }, format="json")
    assert login_resp.status_code == 200
    assert "access" in login_resp.json()
    assert "refresh" in login_resp.json()


@pytest.mark.django_db
def test_token_refresh(api_client, login_user):
    tokens = login_user()
    refresh_resp = api_client.post("/api/auth/token/refresh/", {
        "refresh": tokens["refresh"]
    }, format="json")
    assert refresh_resp.status_code == 200
    assert "access" in refresh_resp.json()


# --------------------
# RESTAURANTS TESTS
# --------------------
@pytest.mark.django_db
def test_create_restaurant(login_user, api_client):
    login_user()
    resp = api_client.post("/api/restaurants/", {"name": "Pizza Place"}, format="json")
    assert resp.status_code == 201
    assert resp.json()["name"] == "Pizza Place"


@pytest.mark.django_db
def test_add_menu(login_user, api_client):
    login_user()
    restaurant = Restaurant.objects.create(name="Sushi Bar")
    resp = api_client.post(f"/api/restaurants/{restaurant.id}/menu/", {
        "date": str(now().date()),
        "items": [{"dish": "Sushi Set", "price": 15}]
    }, format="json")
    assert resp.status_code == 201
    assert resp.json()["items"][0]["dish"] == "Sushi Set"


@pytest.mark.django_db
def test_get_today_menu(api_client, login_user):
    login_user()
    r = Restaurant.objects.create(name="Burger House")
    Menu.objects.create(restaurant=r, date=now().date(), items=[{"dish": "Burger", "price": 10}])

    resp = api_client.get("/api/restaurants/menu/today/")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["items"][0]["dish"] == "Burger"


# --------------------
# VOTES TESTS
# --------------------
@pytest.mark.django_db
def test_vote_for_menu(login_user, api_client):
    login_user()
    r = Restaurant.objects.create(name="Pasta Place")
    m = Menu.objects.create(restaurant=r, date=now().date(), items=[{"dish": "Pasta", "price": 12}])

    resp = api_client.post("/api/votes/", {"menu": m.id}, format="json")
    assert resp.status_code == 201
    assert Vote.objects.count() == 1


@pytest.mark.django_db
def test_vote_only_once_per_day(login_user, api_client):
    login_user()
    r = Restaurant.objects.create(name="Salad Bar")
    m = Menu.objects.create(restaurant=r, date=now().date(), items=[{"dish": "Salad", "price": 8}])
    api_client.post("/api/votes/", {"menu": m.id}, format="json")
    resp = api_client.post("/api/votes/", {"menu": m.id}, format="json")
    assert resp.status_code == 400
    assert "already voted" in str(resp.json()).lower()


@pytest.mark.django_db
def test_vote_results_today(api_client, login_user):
    login_user()
    r1 = Restaurant.objects.create(name="Cafe One")
    m1 = Menu.objects.create(restaurant=r1, date=now().date(), items=[{"dish": "Coffee", "price": 3}])
    r2 = Restaurant.objects.create(name="Cafe Two")
    m2 = Menu.objects.create(restaurant=r2, date=now().date(), items=[{"dish": "Tea", "price": 2}])

    # Голосуємо
    api_client.post("/api/votes/", {"menu": m1.id}, format="json")

    resp = api_client.get("/api/votes/results/today/")
    assert resp.status_code == 200
    data = resp.json()
    assert any(item["restaurant_name"] == "Cafe One" for item in data)
