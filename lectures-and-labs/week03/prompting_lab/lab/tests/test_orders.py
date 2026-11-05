"""The failing test for DIY 8. It fails as you receive it; DIY 8 is about
why, and about what the assistant needs to see before it can tell you."""
from lab.code.orders import order_total


def test_total():
    order = {"items": [{"price": 2.50, "qty": 4}]}
    assert order_total(order) == 10.0
