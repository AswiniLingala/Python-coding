import json

def convert_json_to_python(json_string):
    python_object = json.loads(json_string)  # Use json.loads()
    return python_object

# Example usage:

# 1. JSON string representing a dictionary
json_string_dict = """
{
    "name": "Alice",
    "age": 30,
    "city": "New York"
}
"""
python_object = convert_json_to_python(json_string_dict)
if python_object:
    print("JSON to Python (Dictionary):\n", python_object)
    print(type(python_object))  # Output: <class 'dict'>

# 2. JSON string representing a list
json_string_list = """
[
    1,
    2,
    3,
    "apple",
    "banana"
]
"""
python_object = convert_json_to_python(json_string_list)
if python_object:
    print("\nJSON to Python (List):\n", python_object)
    print(type(python_object))  # Output: <class 'list'>

# 3. JSON string with mixed data types
json_string_mixed = """
{
    "name": "Bob",
    "age": 25,
    "is_student": true,
    "grades": [
        85,
        92,
        78
    ]
}
"""
python_object = convert_json_to_python(json_string_mixed)
if python_object:
    print("\nJSON to Python (Mixed):\n", python_object)
    print(type(python_object))  # Output: <class 'dict'>

