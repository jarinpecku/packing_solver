import sys
import logging

from fastapi import FastAPI

from shipmonk_packer.models import Order, PackerResponse
from shipmonk_packer.packer import ShipmonkPacker


log = logging.getLogger()
log.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.DEBUG)
log.addHandler(stream_handler)


app = FastAPI(title="Shipmonk Packer Microservice",
              description="REST API JSON Python microservice which solves the items packing problem.",
              version="0.1.0",)


@app.get("/app-status")
def app_status() -> dict:
    return dict(message="OK")


@app.post("/order", response_model=PackerResponse)
def post_order(order: Order) -> PackerResponse:
    log.debug("New order: %s", order)
    packer = ShipmonkPacker()
    response = dict(order_id=order.order_id, suitable_boxes=[])
    response["suitable_boxes"] += packer.pack(order)
    return response
