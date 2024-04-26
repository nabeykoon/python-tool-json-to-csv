import json
import xml.etree.ElementTree as ET

# Load JSON schema
with open('schema.json') as f:
    schema = json.load(f)

# Define the fields and rules for XML generation
fields = ['sections']  # Only interested in sections for this XML
# Rules for traversing the schema and extracting data (customize as needed)

# Function to traverse JSON schema and extract data based on fields and rules
def extract_data(schema, fields, rules):
    data = {}
    for field in fields:
        if field in schema:
            data[field] = schema[field]['data']  # Extracting data based on field
            # Additional rules for extracting nested data (if needed)
    return data

# Function to generate XML from extracted data
def generate_xml(data):
    root = ET.Element("sections")  # Root element for XML
    for section in data['sections']:
        section_element = ET.SubElement(root, "section")  # Create XML element for section
        # Populate section element with name and description
        ET.SubElement(section_element, "name").text = section['name']
        ET.SubElement(section_element, "description").text = section['description']
        # Recursively add subsections
        if 'sections' in section:
            generate_subsections(section['sections'], section_element)
        # Add test cases if present
        if 'cases' in section:
            generate_test_cases(section['cases'], section_element)
    return ET.tostring(root, encoding='unicode', method='xml')  # Serialize XML to string

# Function to generate subsections recursively
def generate_subsections(subsections, parent_element):
    for subsection in subsections:
        subsection_element = ET.SubElement(parent_element, "section")  # Create XML element for subsection
        # Populate subsection element with name and description
        ET.SubElement(subsection_element, "name").text = subsection['name']
        ET.SubElement(subsection_element, "description").text = subsection['description']
        # Recursively add subsections
        if 'sections' in subsection:
            generate_subsections(subsection['sections'], subsection_element)
        # Add test cases if present
        if 'cases' in subsection:
            generate_test_cases(subsection['cases'], subsection_element)

# Function to generate test cases
def generate_test_cases(test_cases, parent_element):
    cases_element = ET.SubElement(parent_element, "cases")  # Create XML element for cases
    for case in test_cases:
        case_element = ET.SubElement(cases_element, "case")  # Create XML element for case
        # Populate case element with case attributes
        ET.SubElement(case_element, "id").text = case['id']
        ET.SubElement(case_element, "title").text = case['title']
        ET.SubElement(case_element, "template").text = case['template']
        ET.SubElement(case_element, "type").text = case['type']
        ET.SubElement(case_element, "priority").text = case['priority']
        ET.SubElement(case_element, "estimate").text = case['estimate']
        ET.SubElement(case_element, "references").text = case['references']
        # Add custom elements if present
        if 'custom' in case:
            generate_custom_elements(case['custom'], case_element)

# Function to generate custom elements
def generate_custom_elements(custom, parent_element):
    custom_element = ET.SubElement(parent_element, "custom")  # Create XML element for custom
    # Populate custom element with custom attributes
    if 'automation_status' in custom:
        automation_status_element = ET.SubElement(custom_element, "automation_status")  # Create XML element for automation_status
        ET.SubElement(automation_status_element, "id").text = custom['automation_status']['id']
        ET.SubElement(automation_status_element, "value").text = custom['automation_status']['value']
    if 'test_case_category' in custom:
        test_case_category_element = ET.SubElement(custom_element, "test_case_category")  # Create XML element for test_case_category
        for item in custom['test_case_category']['item']:
            item_element = ET.SubElement(test_case_category_element, "item")  # Create XML element for item
            ET.SubElement(item_element, "id").text = item['id']
            ET.SubElement(item_element, "value").text = item['value']
    if 'automated_test_level' in custom:
        automated_test_level_element = ET.SubElement(custom_element, "automated_test_level")  # Create XML element for automated_test_level
        for item in custom['automated_test_level']['item']:
            item_element = ET.SubElement(automated_test_level_element, "item")  # Create XML element for item
            ET.SubElement(item_element, "id").text = item['id']
            ET.SubElement(item_element, "value").text = item['value']
    if 'preconds' in custom:
        ET.SubElement(custom_element, "preconds").text = custom['preconds']
    if 'steps_separated' in custom:
        steps_separated_element = ET.SubElement(custom_element, "steps_separated")  # Create XML element for steps_separated
        for step in custom['steps_separated']['step']:
            step_element = ET.SubElement(steps_separated_element, "step")  # Create XML element for step
            ET.SubElement(step_element, "content").text = step['content']
            ET.SubElement(step_element, "expected").text = step['expected']

# Main function
def main():
    data = extract_data(schema, fields, {})  # Extract data based on fields and rules
    xml_output = generate_xml(data)  # Generate XML from extracted data
    print(xml_output)  # Print or save XML output to a file

if __name__ == "__main__":
    main()
