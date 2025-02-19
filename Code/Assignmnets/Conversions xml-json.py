import xml.etree.ElementTree as ET
import json

def xml_to_json(xml_string):
    
    root = ET.fromstring(xml_string)
    json_data = {}
    for child in root:
        json_data[child.tag] = child.text
    return json_data

# Example usage:
xml_string = """
<product>
  <name>Laptop</name>
  <price>1200.00</price>
  <in_stock>true</in_stock>
  <category>Electronics</category>
</product>"""

json_output = xml_to_json(xml_string)
print(json.dumps(json_output, indent=4))
