import json
import pandas as pd

# Load the JSON data
with open('testmo-export-grubtech.json', 'r') as json_file:
    data = json.load(json_file)

# Define a function to get custom automation status
def get_custom_automation_status(case_id):
    for case in data['repository_cases']['data']:
        if case['id'] == case_id:
            custom_automation_status_id = case['custom_automation_status']
            for field_value in data['field_values']['data']:
                if field_value['id'] == custom_automation_status_id:
                    return field_value['name']
    return ''

# Define a function to get custom priority
def get_custom_priority(case_id):
    for case in data['repository_cases']['data']:
        if case['id'] == case_id:
            custom_priority_id = case['custom_priority']
            for field_value in data['field_values']['data']:
                if field_value['id'] == custom_priority_id:
                    return field_value['name']
    return ''

# Extracting mapping of field IDs to field names
field_names_map = {field['id']: field['name'] for field in data['fields']['data']}

# Create a dictionary to store test case categories and automation test levels
test_case_categories = {}
automation_test_levels = {}

# Iterate through repository_case_values to populate test_case_categories and automation_test_levels
for case_value in data['repository_case_values']['data']:
    case_id = case_value['case_id']
    field_id = case_value['field_id']
    value_id = case_value['value_id']
    field_name = field_names_map.get(field_id)
    if field_name:
        field_value = None
        for field_value_data in data['field_values']['data']:
            if field_value_data['field_id'] == field_id and field_value_data['id'] == value_id:
                field_value = field_value_data['name']
                break
        if field_value:
            if field_name == 'Automation Test Level':
                if case_id not in automation_test_levels:
                    automation_test_levels[case_id] = []
                automation_test_levels[case_id].append(field_value)
            elif field_name == 'Test Case Category':
                if case_id not in test_case_categories:
                    test_case_categories[case_id] = []
                test_case_categories[case_id].append(field_value)

# Create a dictionary to store section hierarchy
section_hierarchy = {}

# Iterate through repository folders to populate section hierarchy
for folder in data['repository_folders']['data']:
    folder_id = folder['id']
    parent_id = folder['parent_id']
    hierarchy = [folder['name']]
    while parent_id:
        parent_folder = next((f for f in data['repository_folders']['data'] if f['id'] == parent_id), None)
        if parent_folder:
            hierarchy.append(parent_folder['name'])
            parent_id = parent_folder['parent_id']
        else:
            parent_id = None
    section_hierarchy[folder_id] = '/'.join(reversed(hierarchy))

# Create lists to store rows of data
rows = []

# Iterate through repository cases
for case in data['repository_cases']['data']:
    case_id = case['id']
    title = case['name']
    automation_status = get_custom_automation_status(case_id)
    created_by = case['created_by']
    created_on = case['created_at']
    estimate = case['estimate']
    expected_result = case['custom_expected']
    forecast = case['forecast']
    preconditions = case['custom_preconditions']
    priority = get_custom_priority(case_id)
    section_id = case['folder_id']
    section = next((folder['name'] for folder in data['repository_folders']['data'] if folder['id'] == section_id), '')
    section_description = ''
    status = ''
    steps = case['custom_steps_text']

    # Find section description
    for folder in data['repository_folders']['data']:
        if folder['id'] == section_id:
            section_description = folder['docs']
            break

    # Find status
    for state in data['states']['data']:
        if state['id'] == case['state_id']:
            status = state['name']
            break

    # Find test case category
    test_case_category = ", ".join(test_case_categories.get(case_id, []))

    # Find automation test level
    automation_test_level = ", ".join(automation_test_levels.get(case_id, []))

    # Find steps (Expected Result)
    expected_results = []
    for step in data['repository_case_steps']['data']:
        if step['case_id'] == case_id:
            expected_results.append(step['text3'])

    # Find steps (Step)
    steps_steps = []
    for step in data['repository_case_steps']['data']:
        if step['case_id'] == case_id:
            steps_steps.append(step['text1'])

    # Add rows for each step
    max_steps_count = max(len(expected_results), len(steps_steps))
    for i in range(max_steps_count):
        new_row = [
            case_id if i == 0 else '',  # ID column
            title if i == 0 else '',  # Title column
            '' if i != 0 else automation_status,  # Automation Status column (empty for steps after the first one)
            '' if i != 0 else automation_test_level,  # Automation Test Level column (empty for steps after the first one)
            '' if i != 0 else created_by,  # Created By column (empty for steps after the first one)
            '' if i != 0 else created_on,  # Created On column (empty for steps after the first one)
            '' if i != 0 else estimate,  # Estimate column (empty for steps after the first one)
            '' if i != 0 else expected_result,  # Expected Result column (empty for steps after the first one)
            '' if i != 0 else forecast,  # Forecast column (empty for steps after the first one)
            '' if i != 0 else preconditions,  # Preconditions column (empty for steps after the first one)
            '' if i != 0 else priority,  # Priority column (empty for steps after the first one)
            '' if i != 0 else section,  # Section column (empty for steps after the first one)
            '' if i != 0 else section_description,  # Section Description column (empty for steps after the first one)
            '' if i != 0 else status,  # Status column (empty for steps after the first one)
            '' if i != 0 else steps,  # Steps column (empty for steps after the first one)
            expected_results[i] if i < len(expected_results) else '',  # Steps (Expected Result) column
            steps_steps[i] if i < len(steps_steps) else '',  # Steps (Step) column
            '' if i != 0 else test_case_category,  # Test Case Category column (empty for steps after the first one)
            section_hierarchy.get(section_id, '')  # Section Hierarchy column
        ]
        rows.append(new_row)

# Create a DataFrame
df = pd.DataFrame(rows, columns=[
    "ID", "Title", "Automation Status", "Automation Test Level",
    "Created By", "Created On", "Estimate", "Expected Result",
    "Forecast", "Preconditions", "Priority", "Section",
    "Section Description", "Status", "Steps", "Steps (Expected Result)",
    "Steps (Step)", "Test Case Category", "Section Hierarchy"
])

# Export DataFrame to CSV
df.to_csv('test_management_data_export.csv', index=False)
