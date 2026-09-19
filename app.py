from fastapi import FastAPI, HTTPException

from models import Order, OrderCreate
from order_service import OrderNotFoundError, OrderService

app = FastAPI(title="Order Service", version="1.0.0")
service = OrderService()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/orders", response_model=Order, status_code=201)
def create_order(order_data: OrderCreate) -> Order:
    return service.create_order(order_data)


@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int) -> Order:
    try:
        return service.get_order(order_id)
    except OrderNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
