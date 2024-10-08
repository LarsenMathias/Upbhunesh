from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from PIL import Image
import io

# Initialize the Chrome webdriver
driver = webdriver.Chrome()

# Open the webpage
driver.get("https://upbhunaksha.gov.in/")
time.sleep(120)

# Find the canvas element
canvas_element = driver.find_element(By.CSS_SELECTOR, "canvas")

# Get the location and size of the canvas
location = canvas_element.location
size = canvas_element.size

# Take screenshot of the entire webpage
screenshot = driver.get_screenshot_as_png()
image = Image.open(io.BytesIO(screenshot))

# Calculate the coordinates for cropping
top_left = (76.06, 432.97)
bottom_left = (76.06, 63.92)
top_right = (420.7, 432.97)
bottom_right = (420.7, 63.92)

# Convert coordinates to integer
left = int(min(top_left[0], bottom_left[0]))
top = int(min(top_left[1], top_right[1]))
right = int(max(top_right[0], bottom_right[0]))
bottom = int(max(bottom_left[1], bottom_right[1]))

# Crop the image
cropped_image = image.crop((left, top, right, bottom))

# Save the cropped image
cropped_image.save("cropped_canvas_image.png")
time.sleep(1000)
# Close the webdriver
driver.quit()
