import json

def convert_to_json(data):
    json_string = json.dumps(data, indent=4, default=str)  # indent makes it pretty
    return json_string

# 1. Dictionary
my_dict = {"name": "Alice", "age": 30, "city": "New York"}
json_output = convert_to_json(my_dict)
if json_output:
    print("Dictionary to JSON:\n", json_output)

# 2. List
my_list = [1, 2, 3, "apple", "banana"]
json_output = convert_to_json(my_list)
if json_output:
    print("\nList to JSON:\n", json_output)

# 3. Mixed data types
mixed_data = {"name": "Bob", "age": 25, "is_student": True, "grades": [85, 92, 78]}
json_output = convert_to_json(mixed_data)
if json_output:
    print("\nMixed data to JSON:\n", json_output)


# 4. Handling custom objects (Custom object is the instance of class)
class Person
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def to_json(self):  # Custom to_json method
        return {"name": self.name, "age": self.age}

my_person = Person("Charlie", 35)
json_output = convert_to_json(my_person.to_json())  # Call the custom method
if json_output:
    print("\nCustom object to JSON:\n", json_output)
