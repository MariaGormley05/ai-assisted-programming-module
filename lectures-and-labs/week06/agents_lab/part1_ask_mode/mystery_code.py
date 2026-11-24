"""
Mystery Code - Figure out what this does!

DO NOT read the code first. Instead:
1. Select all code (Ctrl+A / Cmd+A)
2. Right-click → Copilot → "Explain This"
3. Read Copilot's explanation
4. Then read the code to verify

Ask Copilot these questions:
- What does this code do?
- Why would someone use a class like this?
- What happens when I call process_order()?
"""


class ShoppingCart:
    """A simple shopping cart to manage items."""
    
    def __init__(self):
        self.items = []
        self.discounts = []
    
    def add_item(self, name, price, quantity=1):
        """Add an item to the cart."""
        self.items.append({
            'name': name,
            'price': price,
            'quantity': quantity
        })
    
    def add_discount(self, percentage):
        """Add a discount percentage (e.g., 10 for 10% off)."""
        self.discounts.append(percentage)
    
    def calculate_subtotal(self):
        """Calculate total before discounts."""
        total = 0
        for item in self.items:
            total += item['price'] * item['quantity']
        return total
    
    def calculate_discount(self, subtotal):
        """Calculate total discount amount."""
        discount_amount = 0
        for discount in self.discounts:
            discount_amount += subtotal * (discount / 100)
        return discount_amount
    
    def calculate_total(self):
        """Calculate final total after discounts."""
        subtotal = self.calculate_subtotal()
        discount = self.calculate_discount(subtotal)
        return subtotal - discount
    
    def display_cart(self):
        """Show what's in the cart."""
        print("\n=== Shopping Cart ===")
        for item in self.items:
            print(f"{item['name']}: ${item['price']} x {item['quantity']}")
        
        subtotal = self.calculate_subtotal()
        discount = self.calculate_discount(subtotal)
        total = self.calculate_total()
        
        print(f"\nSubtotal: ${subtotal:.2f}")
        if discount > 0:
            print(f"Discount: -${discount:.2f}")
        print(f"Total: ${total:.2f}")


def process_order():
    """Create and process a sample order."""
    cart = ShoppingCart()
    
    # Add some items
    cart.add_item("Laptop", 999.99, 1)
    cart.add_item("Mouse", 29.99, 2)
    cart.add_item("Keyboard", 79.99, 1)
    
    # Apply a discount
    cart.add_discount(10)  # 10% off
    
    # Show the cart
    cart.display_cart()
    
    return cart


if __name__ == "__main__":
    order = process_order()
