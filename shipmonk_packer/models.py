from typing import List
from pydantic import BaseModel, Field


example_items = [{"width": 0.9, "height": 0.9, "length": 0.9, "weight": 3, "quantity": 3},
                 {"width": 1.0, "height": 1.0, "length": 1.0, "weight": 5, "quantity": 1},
                 {"width": 0.3, "height": 1.0, "length": 2.55, "weight": 3, "quantity": 1},
                 {"width": 1.0, "height": 1.0, "length": 2.0, "weight": 3, "quantity": 2},
                 ]

example_boxes = [{"id": "3x2x1", "width": 3.0, "height": 2.0, "length": 1.0, "max_weight": 50},
                 {"id": "5x4x2", "width": 5.0, "height": 4.0, "length": 2.0, "max_weight": 50},
                 {"id": "6x6x6", "width": 6.0, "height": 6.0, "length": 6.0, "max_weight": 50},
                 ]


class Item(BaseModel):
    width: float
    height: float
    length: float
    weight: float
    quantity: int


class Box(BaseModel):
    id: str
    width: float
    height: float
    length: float
    max_weight: float


class Order(BaseModel):
    order_id: str = Field(example="89456")
    items: List[Item] = Field(example=example_items)
    boxes: List[Box] = Field(example=example_boxes)


class PackerResponse(BaseModel):
    order_id: str = Field(example="89456")
    suitable_boxes: List[str] = Field(example=["5x4x2", "6x6x6"])
