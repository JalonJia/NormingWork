import os
from selenium import webdriver

# get the path of chromedriver
dir = r'C:\Program Files\Python37\WebDriver' #os.path.dirname(__file__)
chrome_driver_path = dir + '\chromedriver.exe'
#remove the .exe extension on linux or mac platform

# create a new Chrome session
driver = webdriver.Chrome(chrome_driver_path)
driver.implicitly_wait(30)
driver.maximize_window()

# navigate to the application home page
driver.get('http://www.baidu.com/')

# get the search textbox
search_field = driver.find_element_by_name('wd')
search_field.clear()

# enter search keyword and submit
search_field.send_keys('phones')
search_field.submit()

# get all the anchor elements which have product names displayed
# currently on result page using find_elements_by_xpath method
products = driver.find_elements_by_xpath(r'''//*[@id="2"]''')

# get the number of anchor elements found
print('Found ' + str(len(products)) + ' products:')

# iterate through each anchor element and
# print the text that is name of the product
for product in products:
    print(product.text)

# close the browser window
driver.quit()
