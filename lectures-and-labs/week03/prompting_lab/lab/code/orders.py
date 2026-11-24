"""Order totals: the subject of DIY 8."""


def order_total(order: dict) -> float:
    """The total price of every item in the order."""
    return sum(item["unit_price"] * item["qty"] for item in order["items"])
