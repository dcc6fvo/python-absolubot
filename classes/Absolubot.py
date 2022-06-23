from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from string import ascii_lowercase
import time
import subprocess
import sys
import os
import time

class AbsoluBot():

	log=''
	timeout=''
	sleep=''
	output=''

    #Init.. stop all chrome tasks if it exists
	def __init__(self, arg1, arg2, arg3, arg4):

		self.timeout=float(arg1)
		self.sleep=float(arg2)
		self.output=arg3
		self.log=arg4

		if (os.name == 'nt'):
			self.doSomethingWithProcess(['chrome.exe','chromedriver.exe'],'taskkill /im /f')
		else:
			self.doSomethingWithProcess(['chrome','chromedriver'],'killall')
		
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
		chrome_options.add_argument('--blink-settings=imagesEnabled=false')

		return chrome_options 

	#Write all drinks links to a file called "drinks.txt"
	def downloadDrinksLinks(self):

		timeout=self.timeout
		sleep=self.sleep

		drinks = []
		count = 0
		count2 = 0

		if( os.path.exists('links.txt') == False ):
			self.log.logger.info('File links.txt doesn\'t  exist. Scraping the links recipes to links.txt...')
			f = open('links.txt', 'w+')
			for c in ascii_lowercase:
				count2 = count2 + 1

				try:
					self.browser.get('https://www.absolutdrinks.com/en/search/'+c)
					#self.printCode('inicio')
				except WebDriverException as webe: 
					if 'ERR_INTERNET_DISCONNECTED' in webe.msg.upper():
						self.log.logger.error("verify your conenction")
					if 'ERR_NAME_NOT_RESOLVED' in webe.msg.upper():
						self.log.logger.error("verify your DNS")
					sys.exit(1)
				
				try:
					WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located((By.NAME, "year")))
					self.browser.find_element(by=By.NAME, value="year").send_keys('1986')
				except TimeoutException:
					self.log.logger.warning("yearInput not found.")
				except ElementNotInteractableException:
					self.log.logger.warning("yearInput not interactable")
				
				while True:
					try:
						buttonLoadMore = EC.element_to_be_clickable((By.XPATH, "//button[text()='Load more']"))
						WebDriverWait(self.browser, timeout).until(buttonLoadMore)
						elementDrinkList = self.browser.find_elements(by=By.XPATH, value="//section[contains(@class, 'drink-list')]//a[@href]")
						for element in elementDrinkList:
							elementLink = self.removeNonAscii(element.get_attribute('href')) 
							if elementLink not in drinks:
								if ('/with/' not in elementLink):
									drinks.append(elementLink)
									f.write(elementLink)
									f.write('\n')
									count = count + 1

						self.browser.execute_script("arguments[0].click();", WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Load more']"))))
						self.log.logger.info("Found "+str(count)+" drinks recipes")
						time.sleep(sleep)
					except TimeoutException:
						self.log.logger.info("buttonLoadMore not found. finishing the link collector.")
						return
			
				self.log.logger.info("Processing...%"+(str((len(ascii_lowercase))/count2)*100))
			f.close()

			#Finally.. if unix, sort the links and remove /with/ from 'fake' links
			if (os.name != 'nt'):
				cmd = "sort links.txt | grep -v '\/with\/' >> /tmp/links.txt && mv /tmp/links.txt links.txt"
				os.system(cmd)

		else:
			self.log.logger.info('File links.txt already exists. Going on..')
			pass
	
	#Algorithm start 
	def start(self):

		timeout=self.timeout
		sleep=self.sleep

		self.browser.get('https://www.absolutdrinks.com/en/')

		try:
			WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located((By.NAME, "year")))
			self.browser.find_element(by=By.NAME, value="year").send_keys('1986')
		except Exception as e:
			self.log.logger.warning(e.msg+" part: yearInput")

		f = open('links.txt', 'r')
		f2 = open(self.output, 'w+')

		for line in f:
			self.log.logger.info('Processing recipe: '+line.strip())
			self.browser.get(line)

			try:
				self.browser.execute_script("arguments[0].click();", WebDriverWait(self.browser, timeout).
					until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Make this drink']"))))
						
			except Exception as e:
				self.log.logger.warning(e.msg+" part: buttonMakeDrink")
				self.printCode('buttonMakeDrink-not-found.')
				continue
				
			time.sleep(sleep)

			try:
				self.browser.execute_script("arguments[0].click();", WebDriverWait(self.browser, timeout).
					until(EC.element_to_be_clickable((By.XPATH, "//button[@data-measurement='ml']"))))
					
			except Exception as e:
				self.log.logger.warning(e.msg+" part: buttonML")
				self.printCode('buttonML-not-found.')

			time.sleep(sleep)

			try:
				nome = self.browser.find_element(by=By.XPATH, value="//article[contains(@class, 'single-drink')]//h1")				
				ingredientes = self.browser.find_element(by=By.XPATH, value="//article[contains(@class, 'single-drink')]//ul[@class='drink-recipe']")
				ingredientes2 = ingredientes.text.replace('\n',',')

			except Exception as e:
				self.log.logger.warning(e.msg+" part: single-drink")
				self.printCode('nome-not-found')
				continue

			try:
				ingredientesVirgula = self.browser.find_element(by=By.XPATH, value="(//article[contains(@class, 'single-drink')]//p)[1]")
			except NoSuchElementException:
				self.printCode('ingredientesvirgula-not-found')
				ingredientesVirgula = ''

			try:	
				receita = self.browser.find_element(by=By.XPATH, value="(//article[contains(@class, 'single-drink')]//p)[2]")
			except NoSuchElementException:
				self.printCode('receita-not-found')

			f2.write(self.removeNonAscii(nome.text)+';'+self.removeNonAscii(ingredientes2)+';'+self.removeNonAscii(ingredientesVirgula.text)+';'+self.removeNonAscii(receita.text))
			f2.write('\n')

		f2.close()
		f.close()

	def printCode(self,page):
		html = self.browser.page_source
		f = open(page +'.html', 'wb')
		codigoFonte=html.encode('utf-8')
		f.write(codigoFonte)
		f.close()

	def writeTextFile(self,texto):
		f = open(self.output, 'w+')
		f.write(texto)
		f.close()

	def removeNonAscii(self, s): return "".join(i for i in s if ord(i)<126 and ord(i)>31)
	
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
	

	def doSomethingWithProcess(self, lista, comando):
		for proc in lista:
			p = subprocess.Popen([comando, proc], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			response = p.wait()
			if response==0:
				self.log.logger.error(proc+" error..")
			else:
				self.log.logger.info(proc+" ok..")

	def closeBrowser(self):
		self.browser.close()
	
	def __exit__(self, exc_type, exc_value, traceback):
		self.closeBrowser()
