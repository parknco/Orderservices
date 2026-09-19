import pytest

from models import OrderCreate, OrderItem, OrderStatus
from order_service import OrderNotFoundError, OrderService


def sample_order(total_price: float = 100.0) -> OrderCreate:
    return OrderCreate(
        customer_id="customer-123",
        items=[OrderItem(sku="SKU-1", quantity=1, price=total_price)],
    )


def test_create_order_sets_accepted_status_below_5000():
    service = OrderService()

    order = service.create_order(sample_order(4999.99))

    assert order.status == OrderStatus.ACCEPTED


def test_create_order_sets_manual_review_at_5000_boundary():
    service = OrderService()

    order = service.create_order(sample_order(5000.0))

    assert order.status == OrderStatus.MANUAL_REVIEW


def test_calculate_order_total_uses_quantity_and_price():
    service = OrderService()
    payload = OrderCreate(
        customer_id="customer-123",
        items=[
            OrderItem(sku="A", quantity=2, price=10.0),
            OrderItem(sku="B", quantity=3, price=5.0),
        ],
    )

    assert service.calculate_order_total(payload) == 35.0


def test_get_unknown_order_raises_not_found():
    service = OrderService()

    with pytest.raises(OrderNotFoundError):
        service.get_order(999)


def test_mark_shipped_changes_status():
    service = OrderService()
    order = service.create_order(sample_order())

    shipped = service.mark_shipped(order.id)

    assert shipped.status == OrderStatus.SHIPPED
