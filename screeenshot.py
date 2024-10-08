import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import base64

driver = webdriver.Chrome()

driver.get("https://upbhunaksha.gov.in/#home-pane")

# this is only to wait for element
time.sleep(30)
wait = WebDriverWait(driver, 90)
while True:
    try:
        canvas_element = driver.find_element(By.CSS_SELECTOR,"div.ol-viewport canvas")
        break
    except:
        time.sleep(10)

# try to give max time sleep here 

time.sleep(20)
print('taking' )
base64_image = driver.execute_script("return document.querySelector('canvas.ol-unselectable').toDataURL('image/png').substring(21);")
output_image = base64.b64decode(base64_image)

with open("canvas_image.png", 'wb') as f:
    f.write(output_image)
driver.quit()