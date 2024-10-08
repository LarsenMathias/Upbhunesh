import requests
import csv

# File containing the district codes
district_code_file = 'district_codes.txt'

# URL template for the API request
url_template = "https://upbhunaksha.gov.in/stateData/v1/api/LevelData/1?previousCode={}"

# Output file for saving district codes, names, and tehsil numbers
output_file = 'district_tehsil_data.csv'

try:
    # Step 1: Read the district codes from the file
    with open(district_code_file, 'r', encoding='utf-8') as file:
        district_codes = [line.strip() for line in file.readlines()]

    # Prepare a list to store the district code, name, and tehsil data
    district_data_list = []

    # Step 2: Iterate over each district code and make a request
    for code in district_codes:
        # Construct the URL using the district code
        url = url_template.format(code)
        
        # Send GET request to the API
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Print the raw response text
            print(f"Raw response for code {code}:")
            raw_response = response.text.strip()
            print(raw_response)
            
            # Parse the raw response
            district_entries = raw_response.split(',')
            
            # Extract district code and name pairs, and store tehsil data
            for i in range(0, len(district_entries), 2):
                if i < len(district_entries) - 1:  # Ensure we have a name to pair with
                    tehsil_code = district_entries[i].strip()
                    tehsil_name = district_entries[i + 1].strip()
                    
                    # Add a tuple containing district code, tehsil code, and tehsil name
                    district_data_list.append((code, tehsil_code, tehsil_name))
            
            # Print the extracted district codes and names
            print(f"Extracted tehsil data for district code {code}: {district_data_list}")
        else:
            print(f"Failed to retrieve data for code {code}. Status code: {response.status_code}")

    # Step 3: Save all district codes, names, and tehsil numbers to a CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(['District Code', 'Tehsil Code', 'Tehsil Name'])
        # Write each district code, tehsil code, and tehsil name
        for district_code, tehsil_code, tehsil_name in district_data_list:
            writer.writerow([district_code, tehsil_code, tehsil_name])

    print(f"All district codes, tehsil codes, and names saved to {output_file}.")

except Exception as e:
    print("An error occurred:", e)
