from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class OrderStatus(str, Enum):
    ACCEPTED = "ACCEPTED"
    MANUAL_REVIEW = "MANUAL_REVIEW"
    SHIPPED = "SHIPPED"
    CANCELLED = "CANCELLED"


class OrderItem(BaseModel):
    sku: str = Field(min_length=1)
    quantity: int = Field(gt=0)
    price: float = Field(ge=0)


class OrderCreate(BaseModel):
    customer_id: str = Field(min_length=1)
    items: List[OrderItem] = Field(min_length=1)


class Order(BaseModel):
    id: int
    customer_id: str
    items: List[OrderItem]
    total: float
    status: OrderStatus
