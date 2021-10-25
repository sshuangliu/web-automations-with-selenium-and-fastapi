from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import random
#https://github.com/SeleniumHQ/docker-selenium
#https://www.cnblogs.com/nbkhic/p/4885041.html
#docker run -d -p 4444:4444 -p 7900:7900 --shm-size="512m" selenium/standalone-chrome:4.0.0-rc-3-20211010



def selenium_timesheet_instance(username, token):
	current_day = datetime.now().strftime('%d/%m/%Y')
	url = "https://auth.ultimatix.net/utxLogin"
	suburl = 'https://timesheet.ultimatix.net/timesheet'
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument('--disable-gpu')
	driver = webdriver.Remote(
	command_executor="http://172.18.0.2:4444/wd/hub", # the selenium docker's ip add_argument
	desired_capabilities=DesiredCapabilities.CHROME,
	options=chrome_options
	)

	with open('stealth.min.js') as f:
		js = f.read()

	driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
	"source": js
	})

	#driver.implicitly_wait(random.random())
	driver.get(url)

	try:
		select_login_method = WebDriverWait(driver, 10, 0.5).until(
			EC.element_to_be_clickable((By.XPATH, '//*[@id="auth-code-btn"]'))
			)
		if select_login_method:
			select_login_method.click()
	except TimeoutException:
		print("Loading took too much time!")

	try:
		element_process_button = WebDriverWait(driver, 10, 0.5).until(
			EC.element_to_be_clickable((By.XPATH, '//*[@id="proceed-button"]'))
		)

	except TimeoutException:
		print("Loading took too much time!")

	else:
		element_username_input = driver.find_element_by_xpath('//*[@id="form1"]')
		element_username_input.clear()
		element_username_input.send_keys(username)
		element_process_button.click()
		#time.sleep(2)
		try:
			element_token_input = WebDriverWait(driver, 5).until(
			EC.visibility_of_element_located((By.XPATH, '//*[@id="authcode1"]'))
			)
		except TimeoutException:
			print("Loading took too much time!")
		element_token_input.send_keys(token)
		time.sleep(random.random())
		element_login_button = driver.find_element_by_xpath('//*[@id="form-submit"]')
		element_login_button.click()

		# after logined
		driver.get(suburl)
		#time.sleep(3)
		try:
			element_popup = WebDriverWait(driver, 15).until(
			EC.element_to_be_clickable((By.XPATH, '//*[@id="hwModal"]/div[1]/span[2]/img'))
			)
		except TimeoutException:
			print("Loading took too much time!")

		element_popup.click()
		element_effort = driver.find_element_by_xpath('//*[@id="effortforOwnWonSwon11"]')
		element_effort.clear()
		element_effort.send_keys('8')
		element_submit = driver.find_element_by_xpath('//*[@id="layout_pageContent"]/div/div/div[6]/div[2]/div[3]/div[14]/span[1]/input')
		
		try:
			element_submit.click()

		except TimeoutException:
			print("Loading took too much time!")

		time.sleep(3)
		element_effort_value = driver.find_element_by_xpath(f'//*[@id="{current_day}"]')
		result = element_effort_value.text
		#print(result)
		#print(driver.title)
		#print(driver.current_url)
		#driver.save_screenshot('screenshot.png')
	finally:
		driver.quit()
	return result


if __name__ == '__main__':
	one_time_token = input("please a token:")
	selenium_timesheet_instance(username = '1865221', token=one_time_token)