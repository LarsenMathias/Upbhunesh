import requests
import csv

# File containing the district codes
district_code_file = 'district_codes.txt'

# URL templates for the API requests
url_template_level1 = "https://upbhunaksha.gov.in/stateData/v1/api/LevelData/1?previousCode={}"
url_template_level2 = "https://upbhunaksha.gov.in/stateData/v1/api/LevelData/2?previousCode={}"

# Output file for saving district codes, names, tehsil numbers, and village codes
output_file = 'district_tehsil_village_data.csv'

try:
    # Step 1: Read the district codes from the file
    with open(district_code_file, 'r', encoding='utf-8') as file:
        district_codes = [line.strip() for line in file.readlines()]

    # Prepare a list to store the district code, tehsil data, and village codes
    district_data_list = []

    # Step 2: Iterate over each district code to get tehsil data
    for district_code in district_codes:
        # Construct the URL for level 1 (tehsils)
        url_level1 = url_template_level1.format(district_code)

        # Send GET request to the API for tehsil data
        response_level1 = requests.get(url_level1)

        # Check if the request was successful (status code 200)
        if response_level1.status_code == 200:
            print(f"Raw response for district code {district_code}:")
            raw_response_level1 = response_level1.text.strip()
            print(raw_response_level1)
            
            # Parse the raw response for tehsil data
            district_entries = raw_response_level1.split(',')
            
            # Extract tehsil code and name pairs, and store in a temporary list
            tehsil_data = []
            for i in range(0, len(district_entries), 2):
                if i < len(district_entries) - 1:  # Ensure we have a name to pair with
                    tehsil_code = district_entries[i].strip()
                    tehsil_name = district_entries[i + 1].strip()
                    
                    # Add a tuple containing district code, tehsil code, and tehsil name
                    tehsil_data.append((tehsil_code, tehsil_name))

                    # Construct the full previous code for village data
                    previous_code = district_code + tehsil_code

                    # Step 3: Make request to get village data for each tehsil
                    url_level2 = url_template_level2.format(previous_code)
                    response_level2 = requests.get(url_level2)

                    # Check if the request was successful
                    if response_level2.status_code == 200:
                        print(f"Raw response for tehsil {tehsil_code} (previousCode {previous_code}):")
                        raw_response_level2 = response_level2.text.strip()
                        print(raw_response_level2)

                        # Parse the raw response for village data
                        village_entries = raw_response_level2.split(',')

                        # Store village data along with district and tehsil codes
                        for j in range(0, len(village_entries), 2):
                            if j < len(village_entries) - 1:  # Ensure we have a name to pair with
                                village_code = village_entries[j].strip()
                                village_name = village_entries[j + 1].strip()
                                
                                # Add a tuple to the list containing district code, tehsil code, village code, and village name
                                district_data_list.append((district_code, tehsil_code, village_code, village_name))
                    else:
                        print(f"Failed to retrieve village data for {previous_code}. Status code: {response_level2.status_code}")
            
        else:
            print(f"Failed to retrieve tehsil data for district code {district_code}. Status code: {response_level1.status_code}")

    # Step 4: Save all data to a CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(['District Code', 'Tehsil Code', 'Village Code', 'Village Name'])
        # Write each district code, tehsil code, village code, and village name
        for district_code, tehsil_code, village_code, village_name in district_data_list:
            writer.writerow([district_code, tehsil_code, village_code, village_name])

    print(f"All district codes, tehsil codes, village codes, and names saved to {output_file}.")

except Exception as e:
    print("An error occurred:", e)
