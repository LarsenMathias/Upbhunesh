
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import Select
import base64
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("--headless=new") 
driver = webdriver.Chrome(options=options)
driver.maximize_window()
# Open the webpage
driver.get("https://upbhunaksha.gov.in/")
time.sleep(50)
select_level_1 = Select(driver.find_element(By.ID,"level_1"))

# Iterate through each option in level 1
for option_level_1 in select_level_1.options:
    # Select level 1 option
    select_level_1.select_by_visible_text(option_level_1.text)
    
    # Wait for level 2 options to load dynamically
    time.sleep(15)  # Adjust this wait time as needed
    
    # Get level 2 dropdown element
    select_level_2 = Select(driver.find_element(By.ID,"level_2"))
    
    # Iterate through each option in level 2
    for option_level_2 in select_level_2.options:
        # Select level 2 option
        select_level_2.select_by_visible_text(option_level_2.text)
        
        # Wait for level 3 options to load dynamically
        time.sleep(15)  # Adjust this wait time as needed
        
        # Get level 3 dropdown element
        select_level_3 = Select(driver.find_element(By.ID,"level_3"))
        
        # Iterate through each option in level 3
        for option_level_3 in select_level_3.options:
            # Select level 3 option
            select_level_3.select_by_visible_text(option_level_3.text)
            print(option_level_3.text)
            # Wait for the map to load
            time.sleep(15)  # Adjust this wait time as needed
            while True:
                try:
                    canvas_element = driver.find_element(By.CSS_SELECTOR,"div.ol-viewport canvas")
                    break
                except:
                    print("error")
                    time.sleep(1)

            # try to give max time sleep here 

            time.sleep(20)
            print('taking' )
            base64_image = driver.execute_script("return document.querySelector('canvas.ol-unselectable').toDataURL('image/png').substring(21);")
            output_image = base64.b64decode(base64_image)

            with open(option_level_3.text + ".png", 'wb') as f:
                f.write(output_image)
            
            # Find the map element
            # map_element = driver.find_element(By.ID,"map")
            # canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)
            # canvas_png = base64.b64decode(canvas_base64)
            
            # canvas=driver.find_element(By.TAG_NAME,'canvas')
            # print(canvas_png)
            
           



# Close the browser
driver.quit()
