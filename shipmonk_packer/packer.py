from py3dbp import Packer, Bin, Item

from shipmonk_packer.models import Order, List, Box, ShipmonkItem

import logging


log = logging.getLogger()


class ShipmonkPacker:

    def __init__(self):
        self._packer = Packer()

    def _add_boxes(self, boxes: List[Box]):
        log.debug("Adding boxes: %s", boxes)
        for box in boxes:
            self._packer.add_bin(Bin(name=box.id, width=box.width, height=box.height,
                                     depth=box.length, max_weight=box.max_weight))

    def _add_items(self, items: List[ShipmonkItem]):
        log.debug("Adding items: %s", items)
        for idx, item in enumerate(items):
            for item_num in range(item.quantity):
                self._packer.add_item(Item(name=f"item-{str(idx)}-{str(item_num)}", width=item.width,
                                           height=item.height, depth=item.length, weight=item.weight))

    def _get_suitable_boxes(self) -> List[str]:
        suitable_boxes = []
        for packed_bin in self._packer.bins:
            if not packed_bin.unfitted_items:
                suitable_boxes.append(packed_bin.name)
        log.debug("Suitable boxes: %s", suitable_boxes)
        return suitable_boxes

    def pack(self, order: Order) -> List[str]:
        self._add_boxes(order.boxes)
        self._add_items(order.items)
        self._packer.pack()
        return self._get_suitable_boxes()
