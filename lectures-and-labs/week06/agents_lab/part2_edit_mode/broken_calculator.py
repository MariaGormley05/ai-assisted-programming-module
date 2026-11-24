"""
Broken Calculator - Fix the bugs!

This calculator has several bugs. Use Copilot Edit mode to fix them.

Instructions:
1. Try to run the code and see what breaks
2. Select the buggy functions
3. Press Ctrl+I / Cmd+I
4. Ask Copilot to fix the bugs
5. Test the fixed code
"""


class Calculator:
    """A simple calculator with bugs to fix."""
    
    def add(self, a, b):
        """Add two numbers."""
        return a + b
    
    def subtract(self, a, b):
        """Subtract b from a."""
        return a - b
    
    def multiply(self, a, b):
        """Multiply two numbers."""
        # Bug: This doesn't handle the case when b is 0 correctly
        result = 0
        for i in range(b):
            result += a
        return result
    
    def divide(self, a, b):
        """Divide a by b."""
        # Bug: No check for division by zero
        return a / b
    
    def power(self, base, exponent):
        """Raise base to the power of exponent."""
        # Bug: Doesn't handle negative exponents
        result = 1
        for i in range(exponent):
            result *= base
        return result
    
    def factorial(self, n):
        """Calculate factorial of n."""
        # Bug: Doesn't handle negative numbers or 0
        result = 1
        for i in range(1, n):  # Bug: Should be range(1, n+1)
            result *= i
        return result
    
    def average(self, numbers):
        """Calculate average of a list of numbers."""
        # Bug: No check for empty list
        total = sum(numbers)
        return total / len(numbers)
    
    def is_prime(self, n):
        """Check if a number is prime."""
        # Bug: Doesn't handle n <= 1
        for i in range(2, n):
            if n % i == 0:
                return False
        return True


def test_calculator():
    """Test the calculator functions."""
    calc = Calculator()
    
    print("Testing Calculator:")
    print(f"5 + 3 = {calc.add(5, 3)}")
    print(f"10 - 4 = {calc.subtract(10, 4)}")
    print(f"6 * 7 = {calc.multiply(6, 7)}")
    
    # This will cause an error
    try:
        print(f"10 / 0 = {calc.divide(10, 0)}")
    except ZeroDivisionError as e:
        print(f"Error: {e}")
    
    print(f"2 ^ 8 = {calc.power(2, 8)}")
    print(f"5! = {calc.factorial(5)}")
    print(f"Average of [1,2,3,4,5] = {calc.average([1, 2, 3, 4, 5])}")
    print(f"Is 7 prime? {calc.is_prime(7)}")
    print(f"Is 1 prime? {calc.is_prime(1)}")  # Bug: Should handle this


if __name__ == "__main__":
    test_calculator()
