import requests

# URL for the API request
url = "https://upbhunaksha.gov.in/stateData/v1/api/LevelData/0?previousCode="

try:
    # Send GET request to the API
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Print the raw response text
        print("Raw response text:")
        raw_text = response.text
        print(raw_text)
        
        # Step 1: Split the raw text to get district codes and names
        items = raw_text.split(',')
        
        # Step 2: Create a list to store district codes
        district_codes = []
        
        # Step 3: Loop through the items and extract codes (every second item)
        for i in range(0, len(items), 2):
            code = items[i].strip()  # Get the code
            district_codes.append(code)  # Store the code
        
        # Step 4: Save the district codes to a file
        with open('district_codes.txt', 'w', encoding='utf-8') as file:
            for code in district_codes:
                file.write(code + '\n')
        
        print("District codes saved to district_codes.txt")
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
except requests.exceptions.JSONDecodeError as e:
    print("Error decoding JSON:", e)
except Exception as e:
    print("An error occurred:", e)
