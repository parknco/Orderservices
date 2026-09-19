from fastapi.testclient import TestClient

from app import app, service
from order_service import OrderService

client = TestClient(app)


def setup_function():
    # Reset the in-memory service between tests.
    service._orders.clear()
    service._next_id = 1


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_order_api():
    response = client.post(
        "/orders",
        json={
            "customer_id": "customer-123",
            "items": [{"sku": "SKU-1", "quantity": 2, "price": 25.0}],
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["total"] == 50.0
    assert body["status"] == "ACCEPTED"


def test_get_unknown_order_returns_404():
    response = client.get("/orders/999")

    assert response.status_code == 404
