import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.append(str(Path(os.path.dirname(__file__)).parents[1]))

from shipmonk_packer.packer import ShipmonkPacker, Packer
from shipmonk_packer.models import Box, ShipmonkItem, Order


def test__add_boxes():
    box1 = Box(id="3x2x1",width=3.0, height=2.0, length=1.0, max_weight=50)
    box2 = Box(id="5x4x2", width=5.0, height=4.0, length=2.0, max_weight=50)
    box3 = Box(id="6x6x6", width=6.0, height=6.0, length=6.0, max_weight=50)
    boxes = [box1, box2, box3]

    packer = ShipmonkPacker()
    packer._add_boxes(boxes)

    assert len(packer._packer.bins) == 3
    check_bin(box1, packer._packer.bins[0])
    check_bin(box2, packer._packer.bins[1])
    check_bin(box3, packer._packer.bins[2])


def check_bin(box, pbin):
    assert box.id == pbin.name
    assert box.width == pbin.width
    assert box.height == pbin.height
    assert box.length == pbin.depth
    assert box.max_weight == pbin.max_weight


def test__add_items():
    item1 = ShipmonkItem(width=0.9, height=0.9, length=0.9, weight= 3, quantity=3)
    item2 = ShipmonkItem(width=1.0, height=1.0, length=1.0, weight=5, quantity=1)
    item3 = ShipmonkItem(width=0.3, height=1.0, length=2.55, weight=3, quantity=1)
    item4 = ShipmonkItem(width=1.0, height=1.0, length=2.0, weight=3, quantity=2)
    items = [item1, item2, item3, item4]

    packer = ShipmonkPacker()
    packer._add_items(items)

    assert len(packer._packer.items) == 7
    check_item("item-0-0", item1, packer._packer.items[0])
    check_item("item-0-1", item1, packer._packer.items[1])
    check_item("item-0-2", item1, packer._packer.items[2])
    check_item("item-1-0", item2, packer._packer.items[3])
    check_item("item-2-0", item3, packer._packer.items[4])
    check_item("item-3-0", item4, packer._packer.items[5])
    check_item("item-3-1", item4, packer._packer.items[6])


def test__get_suitable_boxes():
    bin1 = MagicMock()
    bin1.unfitted_items = []
    bin1.name = "box1"
    bin2 = MagicMock()
    bin2.unfitted_items = ["eqg"]
    bin2.name = "box2"
    bin3 = MagicMock()
    bin3.unfitted_items = []
    bin3.name = "box3"

    packer = ShipmonkPacker()
    packer._packer.bins = [bin1, bin2, bin3]

    assert packer._get_suitable_boxes() == ["box1", "box3"]


def check_item(name, item, pitem):
    assert name == pitem.name
    assert item.width == pitem.width
    assert item.height == pitem.height
    assert item.length == pitem.depth
    assert item.weight == pitem.weight


def test_pack():
    order = Order(
        order_id="89456",
        items=[{"width": 0.9, "height": 0.9, "length": 0.9, "weight": 3, "quantity": 3},
               {"width": 1.0, "height": 1.0, "length": 1.0, "weight": 5, "quantity": 1},
               {"width": 0.3, "height": 1.0, "length": 2.55, "weight": 3, "quantity": 1},
               {"width": 1.0, "height": 1.0, "length": 2.0, "weight": 3, "quantity": 2}],
        boxes=[{"id": "3x2x1", "width": 3.0, "height": 2.0, "length": 1.0, "max_weight": 50},
               {"id": "5x4x2", "width": 5.0, "height": 4.0, "length": 2.0, "max_weight": 50},
               {"id": "6x6x6", "width": 6.0, "height": 6.0, "length": 6.0, "max_weight": 50}]
    )

    packer = ShipmonkPacker()
    packer._add_boxes = MagicMock()
    packer._add_items = MagicMock()
    packer_mock = MagicMock()
    packer._packer = packer_mock
    packer._get_suitable_boxes = MagicMock(return_value=["box1", "box2"])

    assert packer.pack(order) == ["box1", "box2"]
    packer._add_boxes.assert_called_once_with(order.boxes)
    packer._add_items.assert_called_once_with(order.items)
    packer_mock.pack.assert_called_once()
    packer._get_suitable_boxes.assert_called_once()


