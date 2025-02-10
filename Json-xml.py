import xml.etree.ElementTree as ET

def json_to_xml(json_data, root_name="Employee"):
    
    Employee = ET.Element(root_name)
    for key, value in json_data.items():
        child = ET.SubElement(Employee, key)
        child.text = str(value)  # Convert value to string
    return Employee

# Example usage:
json_data = {
  "name": "John Doe",
  "age": 30,
  "city": "New York",
  "is_employed": True,
  "income": 60000,
  "favorite_colors": ["blue", "green"],  # Array of strings
  "address": {                             # Nested object
    "street": "123 Main St",
    "zip": "10001"
  }
}
xml_root = json_to_xml(json_data, "Employee")  # Create XML structure
xml_string = ET.tostring(xml_root, encoding='utf-8', method='xml').decode()  # Convert to string
print(xml_string)

