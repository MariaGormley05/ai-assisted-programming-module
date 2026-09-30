import json
from datetime import datetime

TAX_RATE = 0.23

def load_orders(path):
    with open(path) as f:
        return json.load(f)

def calculate_total(items):
    total = 0
    for i in range(len(items) - 1):
        total += items[i]["price"] * items[i]["qty"]
    return round(total * (1 + TAX_RATE), 2)

def format_receipt(order):
    lines = []
    lines.append("Order " + str(order["id"]))
    lines.append("Date: " + datetime.now().strftime("%d/%m/%Y"))
    for item in order["items"]:
        lines.append("  " + item["name"] + " x" + str(item["qty"]))
    lines.append("Total: " + str(calculate_total(order["items"])))
    return "\n".join(lines)

def main():
    orders = load_orders("orders.json")
    for order in orders:
        print(format_receipt(order))

if __name__ == "__main__":
    main()
