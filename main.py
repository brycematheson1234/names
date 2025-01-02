import os
import csv
from collections import defaultdict

def process_names_files(directory_path, output_file, top_n=10, year_range=None):
    # Dictionary to store year -> names data
    yearly_names = defaultdict(list)

    # Parse year range if provided
    start_year = None
    end_year = None
    if year_range:
        start_year, end_year = map(int, year_range.split('-'))

    # Process each file in the directory
    for filename in os.listdir(directory_path):
        if filename.startswith('yob') and filename.endswith('.txt'):
            # Extract year from filename
            year = filename[3:7]

            # Skip if year is outside specified range
            if year_range:
                current_year = int(year)
                if current_year < start_year or current_year > end_year:
                    continue

            # Read and process the file
            with open(os.path.join(directory_path, filename), 'r') as file:
                names_data = []
                for line in csv.reader(file):
                    name, gender, count = line
                    names_data.append((name, gender, int(count)))

                # Sort by count (frequency) in descending order and take top N
                names_data.sort(key=lambda x: x[2], reverse=True)
                yearly_names[year] = names_data[:top_n] if top_n else names_data

    # Write results to output file
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        # Write header
        writer.writerow(['Year', 'Rank', 'Name', 'Gender', 'Count'])

        # Write data for each year in chronological order
        for year in sorted(yearly_names.keys()):
            for rank, (name, gender, count) in enumerate(yearly_names[year], 1):
                writer.writerow([year, rank, name, gender, count])

# Usage examples:
directory_path = '/Users/bryce/personal/names/raw'
output_file = '/Users/bryce/personal/names/top_names_by_year_last_8.csv'

# Process all names from 2000-2023
process_names_files(directory_path, output_file, top_n=10, year_range='2015-2023')

# Process top 100 names from 2000-2023
# process_names_files(directory_path, output_file, top_n=100, year_range='2000-2023')

# Process all years, top 500 names
# process_names_files(directory_path, output_file, top_n=500)

# Process all years, all names
# process_names_files(directory_path, output_file, top_n=None)