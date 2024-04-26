import csv

# Open the input and output CSV files
with open('input.csv', 'r', newline='') as csvfile, open('output.csv', 'w', newline='') as outfile:
    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames

    # Write the header to the output file
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    # Iterate over each row in the input CSV
    for row in reader:
        # Split the values in the "Steps (Step)" column by newline character
        steps_step_lines = row['Steps (Step)'].split('\n')
        
        # Determine the number of new rows based on the maximum count of lines in the "Steps (Step)" column
        max_lines = len(steps_step_lines)

        # Split the values in the "Steps (Expected)" column by newline character
        steps_expected_lines = row['Steps (Expected)'].split('\n')

        # Create new rows for each line in the "Steps (Step)" column
        for i in range(max_lines):
            new_row = {}
            for key in fieldnames:
                if key == 'Steps (Step)':
                    new_row[key] = steps_step_lines[i] if i < len(steps_step_lines) else ''
                elif key == 'Steps (Expected)':
                    new_row[key] = steps_expected_lines[i] if i < len(steps_expected_lines) else ''
                else:
                    new_row[key] = row[key] if i == 0 else ''
            writer.writerow(new_row)