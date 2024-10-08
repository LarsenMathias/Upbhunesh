import os
import requests
import csv
import json

# File containing the district, tehsil, and village codes (previously saved)
tehsil_village_file = 'district_tehsil_village_data.csv'

# URL templates for fetching the extent data and WMS map image
url_template_extent = "https://upbhunaksha.gov.in/v1/mapView/MapViewAjaxApiCall/extent/{}?layer_code=UP_PARCEL&districtCode={}"
url_template_wms = "https://upbhunaksha.gov.in/v1/map/wms/{}?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&FORMAT=image%2Fpng&TRANSPARENT=true&layer_code=UP_PARCEL&map_type=GENERIC_MAP&ignore_georef=N&srs=0&auth_key=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJhZjZmODIwNy0yZTBhLTQyMTMtYTc1YS0yMGIwMmY3Y2U1ZWYiLCJpYXQiOjE3MjgzNjM1MDQsImV4cCI6MTcyODM5MjMwNH0.6ohSZh4F5HqTIa4T1ebq_U7idxZ30TLbeDh2iTUdWnV8jK_Qhi4nGHEykETBp-Dlakc6Xd9XiNQlGU4s--WRnw&transparent=true&WIDTH=1024&HEIGHT=1024&SRS=EPSG%3A3857&STYLES=&FORMAT_OPTIONS=dpi%3A113&BBOX={},{},{},{}"

# Output file for saving extent and WMS URL data
output_file = 'district_tehsil_village_extent_wms_data.csv'

# Folder to save images
image_folder = 'images'

# Create the folder if it doesn't exist
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

try:
    # Step 1: Read district, tehsil, and village codes from the CSV file
    district_tehsil_village_list = []
    with open(tehsil_village_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            district_code = row['District Code']
            tehsil_code = row['Tehsil Code']
            village_code = row['Village Code']
            combined_tehsil_code = district_code + tehsil_code  # Combine district and tehsil codes
            district_tehsil_village_list.append((district_code, tehsil_code, village_code, combined_tehsil_code))

    # Prepare a list to store the data
    extent_data_list = []

    # Step 2: Iterate over each district, tehsil, and village code
    for district_code, tehsil_code, village_code, combined_tehsil_code in district_tehsil_village_list:
        # Construct the URL for fetching the map extent data
        url_extent = url_template_extent.format(combined_tehsil_code + village_code, combined_tehsil_code)

        # Send GET request to the API to get the extent data
        response_extent = requests.get(url_extent)

        # Check if the request was successful (status code 200)
        if response_extent.status_code == 200:
            print(f"Raw response for district {district_code}, tehsil {tehsil_code}, village {village_code}:")
            raw_response_extent = response_extent.text.strip()
            print(raw_response_extent)

            try:
                # Parse the JSON response to extract the extent values
                extent_data = json.loads(raw_response_extent)
                ymin = extent_data.get('ymin')
                xmin = extent_data.get('xmin')
                ymax = extent_data.get('ymax')
                xmax = extent_data.get('xmax')

                # Generate the WMS map URL using the extent values
                wms_url = url_template_wms.format(combined_tehsil_code + village_code, xmin, ymin, xmax, ymax)

                # Add the data to the list for saving
                extent_data_list.append((district_code, tehsil_code, village_code, xmin, xmax, ymin, ymax, wms_url))

                # Step 3: Download the image from the WMS URL
                image_filename = f"{district_code}_{tehsil_code}_{village_code}.png"  # Unique file name
                image_path = os.path.join(image_folder, image_filename)

                # Send GET request to download the image
                image_response = requests.get(wms_url)

                if image_response.status_code == 200:
                    # Save the image to the file
                    with open(image_path, 'wb') as image_file:
                        image_file.write(image_response.content)
                    print(f"Image saved for {district_code}, {tehsil_code}, {village_code} at {image_path}")
                else:
                    print(f"Failed to download image for {district_code}, {tehsil_code}, {village_code}. Status code: {image_response.status_code}")

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON for district {district_code}, tehsil {tehsil_code}, village {village_code}: {e}")

        else:
            print(f"Failed to retrieve extent data for {district_code}, {tehsil_code}, {village_code}. Status code: {response_extent.status_code}")

    # Step 4: Save the extent data and WMS URLs into a CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Write the header
        writer.writerow(['District Code', 'Tehsil Code', 'Village Code', 'Xmin', 'Xmax', 'Ymin', 'Ymax', 'WMS URL'])
        # Write each entry of extent data and WMS URL
        for district_code, tehsil_code, village_code, xmin, xmax, ymin, ymax, wms_url in extent_data_list:
            writer.writerow([district_code, tehsil_code, village_code, xmin, xmax, ymin, ymax, wms_url])

    print(f"All extent data and WMS URLs saved to {output_file}.")

except Exception as e:
    print("An error occurred:", e)
