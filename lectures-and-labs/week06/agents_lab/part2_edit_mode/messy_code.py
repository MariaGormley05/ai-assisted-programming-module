"""
Messy Code - Refactor me!

This code works but is poorly written. Use Copilot Edit mode to refactor it.

Instructions:
1. Select all the code
2. Press Ctrl+I / Cmd+I
3. Ask Copilot to refactor following best practices
4. Compare before and after
"""

def _calculate_statistics(numbers):
    total = sum(numbers)
    maximum = 0
    minimum = 0

    for number in numbers:
        if number > maximum:
            maximum = number
        if minimum == 0 or number < minimum:
            minimum = number

    return {
        'avg': total / len(numbers),
        'max': maximum,
        'min': minimum,
        'sum': total,
    }


def calc(numbers):
    return _calculate_statistics(numbers)


def _process_active_item(item):
    value = item['value']
    return {
        'id': item['id'],
        'value': value * 1.1,
        'priority': 'high' if value > 100 else 'low',
    }


def proc_data(data):
    return [
        _process_active_item(item)
        for item in data
        if item['status'] == 'active'
    ]


def _split_by_status(data):
    active_items = []
    inactive_items = []

    for item in data:
        if item['status'] == 'active':
            active_items.append(item)
        else:
            inactive_items.append(item)

    return active_items, inactive_items


def get_stuff(filename):
    # Read file and split items by status.
    import json

    with open(filename, 'r') as file:
        data = json.load(file)

    return _split_by_status(data)


# Test code
if __name__ == '__main__':
    numbers = [10, 20, 30, 40, 50]
    result = calc(numbers)
    print(result)
    
    data = [
        {'id': 1, 'status': 'active', 'value': 150},
        {'id': 2, 'status': 'active', 'value': 80},
        {'id': 3, 'status': 'inactive', 'value': 200},
    ]
    
    processed = proc_data(data)
    print(processed)
