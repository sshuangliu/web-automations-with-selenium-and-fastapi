from helium import *
from selenium.webdriver import ChromeOptions
import time
from datetime import datetime

# https://selenium-python-helium.readthedocs.io/en/latest/index.html
# https://zwbetz.com/download-chromedriver-binary-and-add-to-your-path-for-automated-functional-testing/


#if you need to access google website that are blocked by GFW, you need to set proxy first as follow.
options = ChromeOptions()
#options.add_argument('--proxy-server=127.0.0.1:10809')

current_day = datetime.now().strftime('%d/%m/%Y')
#print(current_day)
username = '1865221'
url = 'https://auth.ultimatix.net/utxLogin'

#start_chrome(url=url, headless=False, options=options)
start_chrome(url=url, headless=True, options=options)
wait_until(Button("Proceed").exists)
write(username, into=S("#form1")) # write base on the HTML element id value
time.sleep(1)
click(Button("Proceed"))  #can also use with press(ENTER)
a = input('please input a one-time token:')
write(a, into=S("#authcode1"))
click(Button("Login"))

#after login suucessful
time.sleep(4)
sub_url = 'https://timesheet.ultimatix.net/timesheet'
go_to(sub_url)
#scroll_down(num_pixels=600)
wait_until(Image("Cancle-Icon").exists)
print('has found the cancle-icon')

#this is used to close Popup
if Image("Cancle-Icon").exists():
	click(Image("Cancle-Icon"))
	print("cannle popup")

time.sleep(1)
#write("8", into=S("#effortforOwnWonSwon11"))
#write("18", into=S('//*[@id="effortforOwnWonSwon11"]'))
write("8", into=S('.textBoxClass ng-pristine ng-valid showClass'))
#highlight(S('//*[@id="effortforOwnWonSwon11"]'))
print('ready to submit')
time.sleep(1)
click(Button("Submit"))

# get the value and confirm
time.sleep(1)
driver = get_driver()
element = driver.find_element_by_id(current_day)
print(element.text)


#kill_browser()

