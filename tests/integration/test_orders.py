import requests
import csv
from pytest_subtests import subtests


BASE_URL = "http://127.0.0.1"


boxes = []
with open("boxes.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        box = dict(id=row["name"], width=float(row["width"]), height=float(row["height"]),
                   length=float(row["length"]), max_weight=float(row["max_weight"]))
        boxes.append(box)

orders = {}
bad_rows = []
with open("orders.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            order_id = row.pop("order_id")
            #if order_id > "22511968":
            #if order_id > "300011968":
            #    break
            if not order_id in orders:
                orders[order_id] = []
            item = dict(width=float(row["width"]), height=float(row["height"]), length=float(row["length"]),
                        weight=float(row["weight"]), quantity=int(row["quantity"]))
            orders[order_id].append(item)
        except Exception as err:
            bad_rows.append(row)
            print(err)



def test_success(subtests):
    for id, items in orders.items():
        data = dict(order_id=id, items=items, boxes=boxes)
        with subtests.test(message=id):
            response = requests.post(url=f"{BASE_URL}/order", json=data)
            assert response.status_code == 200
            print(f"Order {id} response {response.json()}")

    print(f"detected {len(bad_rows)} rows with bad data")
    print(bad_rows)
