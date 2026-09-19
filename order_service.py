from typing import Dict

from models import Order, OrderCreate, OrderStatus


class OrderNotFoundError(Exception):
    pass


class OrderConflictError(Exception):
    pass


class UnauthorizedOrderAccessError(Exception):
    pass


class OrderService:
    """Simple in-memory order service used for the Copilot training demo."""

    def __init__(self) -> None:
        self._orders: Dict[int, Order] = {}
        self._next_id = 1

    @staticmethod
    def calculate_order_total(order_data: OrderCreate) -> float:
        return round(
            sum(item.price * item.quantity for item in order_data.items),
            2,
        )

    def create_order(self, order_data: OrderCreate) -> Order:
        total = self.calculate_order_total(order_data)
        status = (
            OrderStatus.MANUAL_REVIEW
            if total >= 5000
            else OrderStatus.ACCEPTED
        )

        order = Order(
            id=self._next_id,
            customer_id=order_data.customer_id,
            items=order_data.items,
            total=total,
            status=status,
        )
        self._orders[order.id] = order
        self._next_id += 1
        return order

    def get_order(self, order_id: int) -> Order:
        try:
            return self._orders[order_id]
        except KeyError as exc:
            raise OrderNotFoundError(f"Order {order_id} was not found") from exc

    def mark_shipped(self, order_id: int) -> Order:
        order = self.get_order(order_id)
        updated = order.model_copy(update={"status": OrderStatus.SHIPPED})
        self._orders[order_id] = updated
        return updated

    # TRAINING NOTE:
    # Order cancellation is intentionally NOT implemented yet.
    # During the live session, learners can use GitHub Copilot to clarify
    # requirements, plan the change, implement it, generate tests, and debug it.
