# import requests
# res = requests.get('http://192.168.86.36:8080/')

# r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
# print(r.status_code)

import selenium
from selenium import webdriver
import time
import glob

# GLOBALS
driver = selenium.webdriver.Chrome('/Users/neeliyer/Documents/SPOT/parking_bay_detection/detectron2_website/chromedriver 3')
files = glob.glob('/Users/neeliyer/Documents/SPOT/parking_bay_detection_new/mask_RCNN/raw_images/*.*g')
print(files)
website = 'http://localhost:8080/'

for file_name in files:

	# file_name = '/Users/neeliyer/Documents/SPOT/parking_bay_detection_new/mask_RCNN/raw_images/'+str(i)+'.png'
	
	# Open the website
	driver.get(website)

	# Choose File button
	choose_file = driver.find_element_by_name('file')

	# Complete path of the file
	file_location = file_name

	# Send the file location to the button
	choose_file.send_keys(file_location)

	# Find submit button
	submit_button = driver.find_element_by_name('submit')

	# Click submit
	submit_button.click()

	# get screenshot
	save_name = file_name.split('/')[-1].split('.')[0] + '_detectron2_output'
	driver.save_screenshot(save_name+'.png')

	# sleep for a bit- so we don't overexert the cpu
	time.sleep(10)


