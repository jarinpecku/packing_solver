import requests


BASE_URL = "http://127.0.0.1"


example_input = {"order_id": "89456",
                 "items": [{"width": 0.9, "height": 0.9, "length": 0.9, "weight": 3, "quantity": 3},
                           {"width": 1.0, "height": 1.0, "length": 1.0, "weight": 5, "quantity": 1},
                           {"width": 0.3, "height": 1.0, "length": 2.55, "weight": 3, "quantity": 1},
                           {"width": 1.0, "height": 1.0, "length": 2.0, "weight": 3, "quantity": 2},
                           ],
                 "boxes": [{"id": "3x2x1", "width": 3.0, "height": 2.0, "length": 1.0, "max_weight": 50},
                           {"id": "5x4x2", "width": 5.0, "height": 4.0, "length": 2.0, "max_weight": 50},
                           {"id": "6x6x6", "width": 6.0, "height": 6.0, "length": 6.0, "max_weight": 50},
                           ]
                 }

example_output = {"order_id": "89456", "suitable_boxes": ["5x4x2", "6x6x6"]}


def test_success():
    response = requests.post(url=f"{BASE_URL}/order", json=example_input)
    assert response.status_code == 200
    assert response.json() == example_output
