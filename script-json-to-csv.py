# write a python script to extract the data from the json file and write it to a csv file based on the given conditions below
#Input JSON file location: test
#Output CSV file location: output.csv
# Conditions:

# The output CSV file should contain the following columns: "ID","Title","Automation Status","Automation Test Level","Created By","Created On","Estimate","Expected Result","Forecast","Preconditions","Priority","Section","Section Description","Status","Steps","Steps (Expected Result)","Steps (Step)","Test Case Category" which is respective to each test case described in repository_cases 

# The output CSV file should contain the data from the input JSON file with the following matching columns:
# ID: repository_cases.id

# Title: repository_cases.name

# Automation Status: repository_cases.custom_automation_status and get thje string value using field_values.name where field_values.id = repository_cases.custom_automation_status

# Automation Test Level: field_values.name where repository_case_values.case_id = repository_case_values.field_id = repository_case_values.value_id

# Created By: repository_cases.created_by

# Created On: repository_cases.created_at

# Estimate: repository_cases.estimate

# Expected Result: repository_cases.custom_expected

# Forecast: repository_cases.forecast

# Preconditions: repository_cases.custom_preconditions

# Priority: repository_cases.custom_priority

# Section:  repository_folders.name where repository_cases.folder_id = repository_folders.id 

# Section Description: repository_folders.docs where repository_cases.folder_id = repository_folders.id 

# Status: states.name where repository_cases.state_id = states.id

# Steps: repository_cases.custom_steps_text

# Steps (Expected Result) and Steps (Step) are related to each other for given case_id.

# Steps (Expected Result): repository_case_steps.text3 where repository_case_steps.case_id = repository_cases.id
# could be multiple values per repository_cases.id. if so print it in a new row with respect to case_id 

# Steps (Step): export repository_case_steps.text1 where repository_case_steps.case_id = repository_cases.id
# could be multiple values per repository_cases.id. if so print it in a new row with respect to case_id 

# Test Case Category: field_values.name where repository_case_values.case_id = repository_case_values.field_id = repository_case_values.value_id


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
    priority = case['custom_priority']
    section = ''
    section_description = ''
    status = ''
    steps = case['custom_steps_text']

    # Find section and section description
    for folder in data['repository_folders']['data']:
        if folder['id'] == case['folder_id']:
            section = folder['name']
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
            '' if i != 0 else test_case_category  # Test Case Category column (empty for steps after the first one)
        ]
        rows.append(new_row)



# Create a DataFrame
df = pd.DataFrame(rows, columns=[
    "ID", "Title", "Automation Status", "Automation Test Level",
    "Created By", "Created On", "Estimate", "Expected Result",
    "Forecast", "Preconditions", "Priority", "Section",
    "Section Description", "Status", "Steps", "Steps (Expected Result)",
    "Steps (Step)", "Test Case Category"
])

# Export DataFrame to CSV
df.to_csv('test_management_data_export.csv', index=False)















