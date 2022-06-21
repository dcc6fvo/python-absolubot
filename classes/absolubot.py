from socket import timeout
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from string import ascii_lowercase
import time
import sys
import os
import time

class AbsoluBot():

	timeout=''
	sleep=''
	output=''

    #Init.. stop all chrome tasks if it exists
	def __init__(self, arg1, arg2, arg3):

		self.timeout=arg1
		self.sleep=arg2
		self.output=arg3

		if (os.name == 'nt'):
			cmd = 'taskkill /im chrome.exe /f'
		else:
			cmd = 'killall chrome && killall chromedriver'
		os.system(cmd)
		self.browserProfile = self.build_chrome_options()
		self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US', 
			'credentials_enable_service': 'false', 'profile.password_manager_enabled': 'false'})

		#mobile_emulation = { "deviceName": "Nexus 5" }
		#self.browserProfile.add_experimental_option("mobileEmulation", mobile_emulation)
		self.browser = webdriver.Chrome('chromedriver', options=self.browserProfile)

	#Browser parameter configurations 
	def build_chrome_options(self):

		chrome_options = webdriver.ChromeOptions()
		chrome_options.accept_untrusted_certs = True
		chrome_options.assume_untrusted_cert_issuer = True
		# chrome configuration
		# More: https://github.com/SeleniumHQ/docker-selenium/issues/89
		# And: https://github.com/SeleniumHQ/docker-selenium/issues/87
		chrome_options.add_argument("--no-sandbox")
		chrome_options.add_argument("--disable-impl-side-painting")
		chrome_options.add_argument("--disable-setuid-sandbox")
		chrome_options.add_argument("--disable-seccomp-filter-sandbox")
		chrome_options.add_argument("--disable-breakpad")
		chrome_options.add_argument("--disable-client-side-phishing-detection")
		chrome_options.add_argument("--disable-cast")
		chrome_options.add_argument("--disable-cast-streaming-hw-encoding")
		chrome_options.add_argument("--disable-cloud-import")
		chrome_options.add_argument("--disable-popup-blocking")
		chrome_options.add_argument("--ignore-certificate-errors")
		chrome_options.add_argument("--disable-session-crashed-bubble")
		chrome_options.add_argument("--disable-ipv6")
		chrome_options.add_argument("--allow-http-screen-capture")
		chrome_options.add_argument("--start-maximized")
		chrome_options.add_argument("--headless")
		chrome_options.add_argument("--log-level=3")

		return chrome_options 

	#Write all drinks links to a file called "drinks.txt"
	def downloadDrinksLinks(self):
		timeout = float(self.timeout)
		drinks = []
		count = 0
		f = open('drinks.txt', 'w+')
		
		for c in ascii_lowercase:

			self.browser.get('https://www.absolutdrinks.com/en/search/'+c)
			#self.printCode('inicio')

			try:
				yearInput = EC.presence_of_element_located((By.NAME, "year"))
				WebDriverWait(self.browser, timeout).until(yearInput)
			except TimeoutException:
				print("yearInput not found.")
			finally:
				yInput = self.browser.find_element(by=By.NAME, value="year")
				yInput.send_keys('1986')
				yInput.send_keys(Keys.ENTER)
			
			while True:
				try:
					buttonLoadMore = EC.element_to_be_clickable((By.XPATH, "//button[text()='Load more']"))
					WebDriverWait(self.browser, timeout).until(buttonLoadMore)
					aDrinkList = self.browser.find_elements(by=By.XPATH, value="//section[contains(@class, 'drink-list')]//a[@href]")
					for aelement in aDrinkList:
						if aelement not in drinks:
							drinks.append(aelement)
							f.write(aelement.get_attribute('href'))
							f.write('\n')
							count = count + 1
					
					print(count)
					self.browser.execute_script("arguments[0].click();", WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Load more']"))))
					#bLoadMore = self.browser.find_element(by=By.XPATH, value="")
					#bLoadMore.click()
					time.sleep(1)
				except TimeoutException:
					print("buttonLoadMore not found. finishing")
					break
		f.close()
	

	#Algorithm start 
	def start(self, timeout):

		timeout=float(self.timeout)

		self.browser.get('https://www.absolutdrinks.com/en/')

		try:
			yearInput = EC.presence_of_element_located((By.NAME, "year"))
			WebDriverWait(self.browser, timeout).until(yearInput)
		except TimeoutException:
			print("yearInput not found.")
		finally:
			yInput = self.browser.find_element(by=By.NAME, value="year")
			yInput.send_keys('1986')
			yInput.send_keys(Keys.ENTER)

		f = open('drinks.txt', 'r')
		for line in f:
			self.browser.get(line)

			try:
				buttonMakeDrink = EC.element_to_be_clickable((By.XPATH, "//button[text()='Make this drink']"))
				WebDriverWait(self.browser, timeout).until(buttonMakeDrink)
				bbuttonMakeDrink = self.browser.find_element(by=By.XPATH, value="//button[text()='Make this drink']")
				bbuttonMakeDrink.click()
			except TimeoutException:
				print("TimeoutException with buttonMakeDrink.")
			except NoSuchElementException:
				print("buttonMakeDrink not found.")
				self.printCode('buttonMakeDrink-not-found.')
				
			time.sleep(1)

			try:
				buttonML = EC.element_to_be_clickable((By.XPATH, "//button[@data-measurement='ml']"))
				WebDriverWait(self.browser, timeout).until(buttonML)
				bbuttonML = self.browser.find_element(by=By.XPATH, value="//button[@data-measurement='ml']")
				bbuttonML.click()
			except TimeoutException:
				print("TimeoutException with buttonML.")
			except NoSuchElementException:
				print("buttonML not found.")
				self.printCode('buttonML-not-found.')

			time.sleep(1)

			try:
				nome = self.browser.find_element(by=By.XPATH, value="//article[contains(@class, 'single-drink')]//h1")			
			except NoSuchElementException:
				print('page error: '+line)
				self.printCode('nome-not-found')
				continue

			try:	
				ingredientes = self.browser.find_element(by=By.XPATH, value="//article[contains(@class, 'single-drink')]//ul[@class='drink-recipe']")
			except NoSuchElementException:
				self.printCode('ingredientes-not-found')

			try:
				ingredientesVirgula = self.browser.find_element(by=By.XPATH, value="(//article[contains(@class, 'single-drink')]//p)[1]")
			except NoSuchElementException:
				self.printCode('ingredientesvirgula-not-found')
				ingredientesVirgula = ''

			try:	
				receita = self.browser.find_element(by=By.XPATH, value="(//article[contains(@class, 'single-drink')]//p)[2]")
			except NoSuchElementException:
				self.printCode('receita-not-found')

			task = (nome.text, '', ingredientes.text, ingredientesVirgula.text, receita.text)
			print(task)

	def printCode(self,page):
		html = self.browser.page_source
		f = open(page +'.html', 'wb')
		codigoFonte=html.encode('utf-8')
		f.write(codigoFonte)
		f.close()

	def writeTextFile(self,texto):
		f = open('drinks.txt', 'w+')
		f.write(texto)
		f.close()
	
	def get_first_nbr_from_str(self, input_str):
		if not input_str and not isinstance(input_str, str):
			return 0
		out_number = ''
		for ele in input_str:
			if (ele == '.' and '.' not in out_number) or ele.isdigit():
				out_number += ele
			elif out_number:
				break
		return int(out_number)
	
	def closeBrowser(self):
		self.browser.close()
	
	def __exit__(self, exc_type, exc_value, traceback):
		self.closeBrowser()
