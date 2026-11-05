"""
Messy Code - Refactor me!

This code works but is poorly written. Use Copilot Edit mode to refactor it.

Instructions:
1. Select all the code
2. Press Ctrl+I / Cmd+I
3. Ask Copilot to refactor following best practices
4. Compare before and after
"""

def calc(l):
    # Calculate stuff
    x = 0
    y = 0
    z = 0
    for i in l:
        x = x + i
        if i > y:
            y = i
        if z == 0:
            z = i
        else:
            if i < z:
                z = i
    a = x / len(l)
    return {'avg': a, 'max': y, 'min': z, 'sum': x}


def proc_data(data):
    # Process the data
    result = []
    for d in data:
        if d['status'] == 'active':
            temp = {}
            temp['id'] = d['id']
            temp['value'] = d['value'] * 1.1
            temp['priority'] = 'high' if d['value'] > 100 else 'low'
            result.append(temp)
    return result


def get_stuff(filename):
    # Read file and do stuff
    import json
    f = open(filename, 'r')
    data = json.load(f)
    f.close()
    
    active = []
    inactive = []
    
    for item in data:
        if item['status'] == 'active':
            active.append(item)
        else:
            inactive.append(item)
    
    return active, inactive


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
