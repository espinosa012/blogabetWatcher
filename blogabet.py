from __future__										import 	print_function
import  time
import 	datetime
import 	platform
from 	getpass 									import 	getpass
from 	cryptography.fernet 						import Fernet
from 	os 											import path

from 	bet_markets 								import 	set_market_and_bet, print_pick

from 	bs4 										import 	BeautifulSoup
from 	selenium.webdriver 							import 	Chrome
from    selenium.webdriver.support.wait     		import 	WebDriverWait
from    selenium.webdriver.chrome.options   		import 	Options
from 	selenium.webdriver.common.keys 				import 	Keys
from 	selenium.webdriver.common.by 				import 	By
from 	selenium.webdriver.support 					import 	expected_conditions as EC
from 	selenium.webdriver.common.action_chains 	import 	ActionChains



class Blogabet(object):
	email 				=	''
	password 			=	''

	driver 				=	None

	logged_in 			=	False
	most_recent_pick 	=	None
	
	def __init__(self):
		self.email, self.password   	=	self.get_credentials()
		self.driver 					=	self.get_driver()
		

	def get_driver(self):
		options 		= 	Options()

		#	Comment this line to not headless web navigator
		options.add_argument('--headless')

		webdriver_path 		= 	'webdriver/chromedriver'
		if 'Win' in str(platform.system()):
			webdriver_path	=	webdriver_path+'.exe'

		try:
			driver 	=	Chrome(executable_path=webdriver_path, chrome_options=options)
			driver.maximize_window()
			return driver

		except Exception as e:
			raise Exception('Could not get webdriver ({}), please download webdriver for your platform from https://chromedriver.chromium.org/'.format(e))





	def blogabet_login(self):
		if not self.email or not self.password:
			raise Exception('Credentials error.')

		self.driver.get('https://blogabet.com/')

		#	Login 
		login_button	=	'.//*[contains(text(), "LOG IN")]'
		WebDriverWait(self.driver,50).until(EC.presence_of_element_located((By.XPATH, login_button))).click()

		login_form 		=	WebDriverWait(self.driver,50).until(EC.presence_of_element_located((By.CLASS_NAME, "form-horizontal")))	
		
		time.sleep(0.6)
		print('Login into blogabet...')
		time.sleep(0.6)
		login_form.find_elements_by_tag_name('input')[0].send_keys(self.email)
		time.sleep(0.6)
		login_form.find_elements_by_tag_name('input')[1].send_keys(self.password + Keys.TAB + Keys.RETURN)
		

		print('Login done')
		self.logged_in 	=	True
	





	def get_last_pick_in_feed(self, my_tipsters=True):
		#	Si my_tipsters = False, obtiene los picks del feed general de blogabet, en vez de aquellos de los tipsters a los que seguimos
		if my_tipsters:
			WebDriverWait(self.driver,50).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "My tipsters")]'))).click()

		time.sleep(2)

		media_list_xpath	=	'.//*[contains(@class, "media-list")]'

		#	Elementos html correspondientes a los picks
		picks_in_feed		=	WebDriverWait(self.driver,50).until(EC.presence_of_element_located((By.XPATH, media_list_xpath))).find_elements_by_tag_name('li')
		try:
			last_pick_in_feed 	= 	self.get_pick_from_html(picks_in_feed[0])
			return last_pick_in_feed

		except Exception as e:
			raise e







	def get_pick_from_html(self, elem):
		#	Recibe el elemento <li> en el que se encuentra el pick del feed y forma el objeto
		pick 	=	{}

		soup 	=	BeautifulSoup(elem.get_attribute('innerHTML'), 'html.parser')

		if 'Click here to see the pick' in soup:
			#	Pinchamos en 'here' y scrapeamos el pick 
			return None


		pick['url']		=	soup.find('a', {'class':'report enable-tooltip'})['data-url']
		pick['tipster']	=	pick['url'].split('.')[0].split('//')[1]
		
		if soup.find('i', {'class':'fa-plus-square'}):
			pick['type']=	'combo_pick'
			return pick
		
		pick['match']	=	soup.find('a', {'href':pick['url']}).text.replace(' - ',' v ')

		pick_odds 		=	soup.find('div', {'class':'pick-line'}).text
		pick['pick']	=	pick_odds.split('@')[0].strip()
		pick['odds']	=	pick_odds.split('@')[1].strip()
		pick['stake']	=	soup.find('span', {'class':'label label-default'}).text.strip()
		pick['booker']	=	soup.find('a', {'class':'label label-primary'}).text.strip()

		type_kickoff	=	soup.findAll('small', {'class':'text-muted'})[1].text.strip()

		pick['type']	=	type_kickoff.split('/')[0].strip() + ' - ' + type_kickoff.split('/')[1].strip()
		pick['kickoff']	=	type_kickoff.split('/')[2].strip().replace('Kick off: ','')
		pick['isLive']	=	('Livebet' in pick['type'])	

		pick['date']	=	datetime.datetime.now().replace(microsecond=0).strftime("%m/%d/%Y %H:%M:%S")

		try:
			pick['market']	=	''
			pick['bet']		=	''
			pick 			=	set_market_and_bet(pick)

			return pick
			
		except Exception as e:
			raise e
			



	def compare_picks(self,p1, p2):
		#	Returns True if p1 and p2 are different (it uses 'url' field to set equality)
		return p1['url'] != p2['url']
		


	def watch_blogabet_feed(self):
		if not self.logged_in:
			raise Exception('Log in into blogabet.com to watch your feed')
		
		print('Watching feed')
		self.most_recent_pick 	=	self.get_last_pick_in_feed(self.driver)

		print('Last pick in feed:')
		print_pick(self.most_recent_pick)

		while True:
			# Actualizar last_pick cuando llega uno nuevo
			try:
				new_pick 	=	self.get_last_pick_in_feed()
				if self.compare_picks(self.most_recent_pick, new_pick):
					#	new pick in feed
					print('New pick in feed ({})'.format(new_pick['date']))
					self.most_recent_pick 	= 	new_pick


					#	Implement here what to do when a new pick appears in feed
					print_pick(new_pick)

			except Exception as e:
				raise e
			



	def get_credentials(self, email_path='credentials/email.txt', secret_key_path='credentials/secret.key'):
		try:
			if path.exists(email_path):
				email 	=	open(email_path, 'r').read().strip()
			else:
				email 	=	input('Type your blogabet email: ').strip()
				open(email_path, 'w').write(email)

			password 	=	self.decrypt_password()

		except Exception as e:
			raise e


		return email, password



	########################################################################################################
	####### Encrypt/Decrypt password      ##################################################################
	########################################################################################################


	def generate_key(self, secret_key_path='credentials/secret.key'):
		#	Generates a key and save it into a file
	    key 	= 	Fernet.generate_key()
	    with open(secret_key_path, 'wb') as key_file:
	        key_file.write(key)
	        key_file.close()



	def load_key(self, secret_key_path='credentials/secret.key'):
		#	Loads key from file and returns as a string
		if path.exists(secret_key_path):
			return open(secret_key_path, "rb").read()
		else:
			self.generate_key(secret_key_path)
			return open(secret_key_path, "rb").read()





	def encrypt_password(self, encrypted_password_path='credentials/password.key'):
		if path.exists(encrypted_password_path):
			return open(encrypted_password_path, 'r').read().strip().encode()

		else:
			password 	= 	getpass('Type your blogabet password: ').strip().encode()
			f 			= 	Fernet(self.load_key())

			encrypted_password 	= 	f.encrypt(password)

			#	Write encrypted password into a file
			encrypted_password_file 	=	open(encrypted_password_path, 'wb')
			encrypted_password_file.write(encrypted_password)

			return encrypted_password




	def decrypt_password(self, encrypted_password=''):
	    '''
	    Decrypts an encrypted message and returns it as a string
	    '''
	    if not encrypted_password:
	    	encrypted_password 	=	self.encrypt_password()

	    f 	= 	Fernet(self.load_key())
	    decrypted_password 	= 	f.decrypt(encrypted_password).decode()

	    return decrypted_password



