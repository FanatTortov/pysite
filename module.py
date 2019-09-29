# -*- coding: utf-8 -
import random
import time
import threading
import sys
import json
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.proxy import Proxy, ProxyType
from telethon import TelegramClient, sync
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.tl.types import InputPhoneContact
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.functions.channels import InviteToChannelRequest
from PIL import Image
import sendcaptcha


sys.path.insert(1, '/home/fanat_tortov/Документы/selenium/names')
from get_name import *

def checkJson(js):
	try:
		return json.loads(js)['Answer']
	except:
		return None

class ProxyManager:
	def __init__(self):
		self.prox_arr = []
		self.proxy = None

	def _getProxyList(self):
		r = requests.get('https://trast.in.ua/?servis=proxy&act=proxy')
		return checkJson(r.text)


	def getProxy(self):
		self.proxy = None
		if len(self.prox_arr)>0:
			self.proxy = self.prox_arr.pop(0)
		prox_list = self._getProxyList()
		if ((prox_list is None or len(prox_list)<=0) and self.proxy is None):
			return None
		threads = []
		for i in prox_list:
			new_thread = threading.Thread(target=self._threadProxy, args=(i,))
			threads.append(new_thread)
			new_thread.daemon = True
			new_thread.start()
		if self.proxy is None:
			activeThread = 1
			while (activeThread>0 and len(self.prox_arr)==0):
				activeThread = 0
				for i in threads:
					if not i.isAlive():
						threads.remove(i)
					else:
						activeThread+=1
				time.sleep(0.2)
			if len(self.prox_arr)<=0:
				self.proxy = self.getProxy()
			else:
				self.proxy = self.prox_arr.pop(0)
		return self.proxy

		#######################################

	def removeProxy(self):
		updProxy(self.proxy,0)
		self.proxy = self.getProxy()

	def _threadProxy(self,proxy,timeout=15,save=False):

		proxies = {'http': 'http://'+proxy['proxy'],'https': 'https://'+proxy['proxy']}
		s = requests.session()
		s.proxies.update(proxies)
		try:
			r = s.get("https://habr.com",timeout=timeout)
			if (r.status_code==200 and len(r.text)>0):
				if len([i for i in self.prox_arr if i==proxy])==0:
					self.prox_arr.append(proxy.copy())
					return updProxy(proxy,1,save,timeout)
				return True
			return updProxy(proxy,0,save,timeout)
		except:
			return updProxy(proxy,0,save,timeout)

def updProxy(proxy,state=1,save=False,timeout=15):
	url = 'http://trast.in.ua/?servis=proxy&act='
	pr = requests.utils.quote(proxy['proxy'], safe='')
	if (save and state==1):
		try:
			requests.get(url+"add&proxy="+pr,timeout=timeout)
			return True
		except:
			return False
	try:
		requests.get(url+"update&id="+proxy['id']+"&status="+str(state),timeout=timeout)
		return True
	except:
		return False

class User:
	def __init__(self,link,func=None,hide=True,timeoutLoadPage=60,create=True,ID=-1,browser='Chrome'):
		self.link = link
		self.create = create
		self.browser = browser
		self.ID = ID
		self.phoneNumb = None
		if create:
			self.person = Person()
			self.proxy_man = ProxyManager()
			self.proxy_man.getProxy()
			self.changeUserMark()

		else:
			if ID>0:
				self._load()
				self.person = Person(link,ID)
			else:
				pass
				#eror return
		self.brow = Brow(self,func,timeoutLoadPage,hide)

	def number(self,arr=None):
		if arr is not None:
			self.phoneCntr = '+'+arr[0] if arr[0].find('+')<0 else arr[0]
			self.phoneNumb = arr[1]
		elif self.phoneNumb is not None:
			return self.phoneCntr,self.phoneNumb
		return ()

	def changeUserMark(self):
		self.us_ag = self._genUs_ag()
		self.mon_size = self._genMon_sz()

	def _genMon_sz(self):
		f = open('/home/fanat_tortov/Документы/scripts/mon-size','r')
		arr = f.read().split('\n')
		rand = random.randint(0,100)
		for i in arr:
			rand -= int(i.split(' ')[2])
			if rand<0:
				return [int(k) for k in i.split(' ')[:-1]]
		return [int(k) for k in arr[-1].split(' ')[:-1]]

	def _genUs_ag(self):
		b = self.browser
		if b=="Chrome":
			r = requests.get('https://trast.in.ua/user_agent.php')
			if r.status_code==200:
				return r.text
			return None
		elif b=="Firefox":
			return "Fox"
		else:
			pass

	def _load(self):
		pass

	def __str__(self):
		return "link:"+self.link+" proxy:"+self.proxy_man.proxy['proxy']+" useragent:"+self.us_ag

class Sim5Worker:
	def __init__(self):
		__rawApi = ['eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1OTkyNDQzMDksImlhdCI6MT',
		'U2NzcwODMwOSwicmF5IjoiYmRiMzM2NjJlNDAzZDBhMzkzOTI4OTg1NDUwMzJlOTEiLCJzd',
		'WIiOjIyMDEwMH0.ybu8Hz0HBZguJvjpo4UP5dw0XwzF2rFjaEoy7UakqLiylh3fc97wMh_p',
		'vtf_cP3iRkKyGS9DpJv-e-qxDeYGfI98N5UqsYIu3hCrlx72aHKZSdqJpH95YY83aoeQ4WU',
		'JxJm9fd-EP4kBXLuNZfIxkBcsRrqwOVSCsx3JiJ0n0yyAmC928h-2AeNHN-Kj69gqw2rBBK',
		'xqtcDFrb6tnQT3eerb-MYdWEP1gAFVExPa1ay2N1cTteFFxo0pAtGdambWlyTLm34SYqhLM',
		'xqYMLKUYBtuuPAurXm472eFVFyZOVLLUL3AVTGtQT1mdxUu7LbM_qUW7Lm8_KXT0VCG2JFTuw']
		self.token = 'Bearer '+"".join(__rawApi)
		self.rawServInfo = [None,time.time()]
		self.numberInfo = None
		self._code = None
		self._getInfo(True)

	def __str__(self):
		return json.dumps(self.telegram)

	def _getInfo(self,new=False):
		if new:
			url = 'https://5sim.net/v1/guest/products/any/any'
			res = None
			r = requests.get(url,headers={'Authorization':self.token})
			if (r.text and r.status_code==200):
				try:
					res=json.loads(r.text)['telegram']
				except:
					pass
			if (res is not None):
				self.rawServInfo = [res,time.time()]
		else:
			if (self.rawServInfo[0]==None or time.time()-self.rawServInfo[1]>1):
				self._getInfo(True)
		return self.rawServInfo[0]

	def buyNumber(self):
		if (self.tgCount>0 and self.balance-self.tgPrice>0 and self.tgPrice<5):
			self.numberInfo = None
			self._code = None
			url = 'https://5sim.net/v1/user/buy/activation/any/any/telegram'
			res = None
			r = requests.get(url,headers={'Authorization':self.token})
			if (r.text and r.status_code==200):
				try:
					self.numberInfo=json.loads(r.text)
					res = True
				except:
					pass
			return res
		else:
			return None

	def _getCode(self):
		if self._code is None:
			if (self.numberInfo is not None):
				ID = str(self.numberInfo['id'])
				url = 'https://5sim.net/v1/user/check/'+ID
				while (self._code is None and self.numberInfo['status']!='TIMEOUT'):
					r = requests.get(url,headers={'Authorization':self.token},timeout=15)
					if (r.text and r.status_code==200):
						try:
							self.numberInfo=json.loads(r.text)
							self._code = self.numberInfo['sms'][0]['code']
						except:
							pass
					time.sleep(1)
				if (self._code is not None):
					self._finishBuy()
		return self._code

	def _finishBuy(self):
		ID = str(self.numberInfo['id'])
		url = 'https://5sim.net/v1/user/finish/'+ID
		requests.get(url,headers={'Authorization':self.token},timeout=15)
		return True

	def _servCount(self):
		return self.telegram['Qty'] if self.telegram is not None else None

	def _getNumber(self):
		return self.numberInfo['phone'] if self.numberInfo is not None else None

	def _getCountry(self):
		if self.numberInfo is not None:
			if (self.numberInfo['country']=='kazakhstan'):
				return "+77"
			if (self.numberInfo['country']=='russia'):
				return "+7"
			return self.tgPhone[:2]
		else:
			return None

	def _servPrice(self):
		return self.telegram['Price'] if self.telegram is not None else None

	def _checkBal(self):
		url = 'https://5sim.net/v1/user/profile'
		r = requests.get(url,headers={'Authorization':self.token})
		if (r.text and r.status_code==200):
			try:
				return float(json.loads(r.text)['balance'])
			except:
				return None
		return None

	balance = property(_checkBal)
	telegram = property(_getInfo)
	tgCount = property(_servCount)
	tgPrice = property(_servPrice)
	tgPhone = property(_getNumber)
	tgCode = property(_getCode)
	tgCountry = property(_getCountry)

class TelethonWorker:
	def __init__(self,api,hash_,number,password,proxy,getCodeFunc):
		self.api_id =  api
		self.api_hash = hash_
		self.proxy = proxy
		proxy_ip = self.proxy.split(':')[0]
		port = self.proxy.split(':')[1]
		self.getCode = getCodeFunc
		self.number = number
		self.session =  number
		self.password = password
		self.app = TelegramClient(self.session, self.api_id, self.api_hash, proxy = (socks.SOCKS5, str(proxy_ip), int(port)))
		self.app.run_until_disconnected()
		self.app.start(phone=self.number,password=self.password,code_callback=self.getCode)
		# self.app.start()

	def getListMembers(self):
		users = []
		for dialog in self.app.get_dialogs():
			if(dialog.is_group and type(dialog.draft.entity).__name__=="Channel"):
				time.sleep(10)
				chatUser = self.app.get_participants(dialog,aggressive=True)
				for user in chatUser:
					if(not(user.bot or user.is_self or user.deleted)):
						users.append(user)
		return self.saveListUsers(users)

	def saveListUsers(self,arr):
		f = open('users.txt','w')
		for i in arr:
			username = "@"+i.username if i.username is not None else "-"
			f.write(str(i.id)+"\t"+username+'\n')
		f.close()
		return len(arr)

class Person:
	def __init__(self,new=True,link=None,ID=None):
		if new:
			self._generate()
		else:
			_load(link,ID)

	def _load(self,link,ID):
		pass

	def _generate(self):
		self.rawPerson = getNAME().split(' ')
		self.password = createPass(12)
		self.rusName = self.rawPerson[1]
		self.rusSurName = self.rawPerson[0]
		self.menState = self.rawPerson[2]!='Ж'
		self.latName = self.rawPerson[4]
		self.latSurName = self.rawPerson[3]
		self.date = self.rawPerson[5].split('.')
		self.mounth = self.date[1]
		self.day = self.date[-1]
		self.year = self.date[0]

	def getTitle(self,length = 6):
		try:
			return self.title
		except:
			self.shortName = createName(1,length)
			self.title = self.shortName+' '+createName(0,length)
			return self.title



	def __str__(self):
		return " ".join(self.rawPerson)

def createPass(n=10):
    s = ""
    for _ in range(n):
        r = random.randint(0,61)
        if r<10:
            r+=48
        elif r<36:
            r+=65-10
        else:
            r+=97-36
        s+=chr(r)
    return s

def createName(bigL=True,n=5):
    n += random.randint(0,3)
    s = ""
    lit = 'eyuioa'
    gho = 'qwrtpsdfghjklzxcvbnm'

    ifa = random.randint(0,2)==0
    while n>0:
        s+= lit[random.randint(0,len(lit)-1)] if (ifa) else gho[random.randint(0,len(gho)-1)]
        s = s.upper() if (bigL and len(s)==1) else s
        ifa = not ifa
        n -=1
        s+= 'u' if (s[-1]=='q') else ''
    return s


class Brow:
	def __init__(self,user,func,timeoutLoadPage,hide):
		self.autoHide = hide
		self.user = user
		self.timeout = timeoutLoadPage
		self.brow = False
		self.func = func if (func is not None) else self._deffunc


	def init(self):
		for _ in range(5):
			if self._openBrow():
				return True
		return False

	def _deffunc(self):
		return True

	def getSite(self,link):
		try:
			self.brow.get(link)
			return True
		except:
			return False

	def _visitSite(self):
		if self.getSite(self.user.link):
			return self.func(self)
		return False

	def _openBrow(self):
		opts = webdriver.ChromeOptions()
		platform = ""
		if self.user.us_ag.find('Windows')>0:
			platform='Win32'
		if self.user.us_ag.find('Macintosh')>0:
			platform='Macintosh'
		if self.user.us_ag.find('Linux')>0:
			platform='Linux x86_64'

		opts.add_argument("user-agent="+self.user.us_ag)
		opts.add_argument("platform="+self.user.us_ag)
		opts.add_argument('--disable-infobars')
		opts.add_argument('--disable-extensions')
		opts.add_argument("--start-maximized")
		opts.add_argument("--ignore-certificate-errors")
		opts.add_argument("--disable-popup-blocking")
		opts.add_argument("window-size="+str(self.user.mon_size[0])+','+str(self.user.mon_size[0]))
		opts.add_argument("--enable-precise-memory-info")
		opts.add_argument("--no-sandbox")
		opts.add_argument("--disable-setuid-sandbox")
		opts.add_argument("--disable-seccomp-filter-sandbox")
		opts.add_argument("--disable-ipv6")
		opts.add_argument("--disable-notifications")

		prefs = {"profile.default_content_setting_values.notifications" : 2}
		prefs = {"credentials_enable_service", False}
		prefs = {"profile.password_manager_enabled" : False}
		opts.add_experimental_option("prefs",prefs)
		opts.add_experimental_option("excludeSwitches", ['enable-automation'])

		prox = Proxy()
		prox.proxy_type = ProxyType.MANUAL
		prox.http_proxy = self.user.proxy_man.proxy['proxy']
		prox.ssl_proxy = self.user.proxy_man.proxy['proxy']

		capabilities = webdriver.DesiredCapabilities.CHROME
		prox.add_to_capabilities(capabilities)

#webdriver=''
		self.brow = webdriver.Chrome(executable_path='/home/fanat_tortov/Документы/selenium/chromedriver',desired_capabilities=capabilities,chrome_options=opts)

		# self.brow.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent":self.user.us_ag, "platform":platform})

		h,w=self.user.mon_size
		self.brow.set_window_rect(0,0,h,w)
		if self.autoHide:
			self.minWin()

		self.brow.set_page_load_timeout(self.timeout)
		self.brow.implicitly_wait(10)


		if not self._visitSite():
			self.brow.quit()
			self.user.proxy_man.removeProxy()
			self.user.changeUserMark()
			return False
		return True

	def __str__(self):
		return self.brow.current_url

	def minWin(self):
		try:
			self.brow.minimize_window()
			return True
		except:
			return False

	def maxWin(self):
		try:
			self.brow.maximize_window()
			return True
		except:
			return self.maxWin()

	###################################################################################
	def _argsValidate(self,*args):
		el = self.brow
		searchStr = args[0]
		ind = None
		if len(args)==3:
			el = args[0]
			searchStr = args[1]
			ind = args[-1]
		if len(args)==2:
			if isinstance(args[0], WebElement):
				el = args[0]
				searchStr = args[1]
			else:
				searchStr = args[0]
				ind = args[-1]
		return (el,searchStr,ind)

	def _selenFindByFunc(self,func,searchStr,ind):
		try:
			els = func(searchStr)
			if ind is not None:
				if len(els)>ind:
					return els[ind]
				return els[-1]
			elif len(els)>0:
				return els
			return False
		except:
			return False

	def finds_by_class(self,*args):
		el,searchStr,ind = self._argsValidate(*args)
		return self._selenFindByFunc(el.find_elements_by_class_name,searchStr,ind)


	def finds_by_tag(self,*args):
		el,searchStr,ind = self._argsValidate(args)
		return self._selenFindByFunc(el.find_elements_by_tag_name,searchStr,ind)


	def finds_by_name(self,*args):
		el,searchStr,ind = self._argsValidate(args)
		return self._selenFindByFunc(el.find_elements_by_name,searchStr,ind)



	def find_by_id(self,_id):
		try:
			return self.brow.find_element_by_id(_id)
		except:
			return False

	def click_by_id(self,_id):
		try:
			el = self.find_by_id(_id)
			return self.click(el)
		except:
			return False

	def click_by_class(self,*args):
		return self.find_by_func(self.finds_by_class,*args)

	def click_by_tag(self,*args):
		return self.find_by_func(self.finds_by_tag,*args)

	def click_by_name(self,*args):
		return self.find_by_func(self.finds_by_name,*args)

	def find_by_func(self,func,*args):
		el = func(*args)
		if isinstance(el,list):
			el = el[0]
		try:
			return self.click(el)
		except:
			return False


	def select_value(self,el,val):
		try:
			sel = Select(el)
			sel.select_by_value(val)
			return True
		except:
			return False


	def click(self,el):
		try:
			hover = ActionChains(self.brow).move_to_element(el)
			hover.click(el)
			hover.perform()
			return True
		except:
			return False

	def send_keys(self,el,txt):
		try:
			el.clear()
			el.send_keys(txt)
			return True
		except:
			return False


	def get_attribute(self,el,attr):
		try:
			return el.get_attribute(attr)
		except:
			return False

	def logs(self,txt):
		print(txt)

####################################################################################

def getCaptchaText(cpath):
	ru_captcha = sendcaptcha.RUCaptcha(apikey="ced266da9c3a256af63673ef09f3e607") ####WRONG API ced266da9c3a256af63673ef09f3e607
	value = ru_captcha.parse(path=cpath)

	while not value.is_ready():
	    time.sleep(2)
	#
	answ = value.get_value()
	ru_captcha.dispose()
	return answ

def saveCaptchaImage(brow,size,location):
	cappath = 'image/'+createPass()+createPass()+'.png'
	brow.screenshot(cappath)

	im = Image.open(cappath) # uses PIL library to open image in memory

	left = location['x']
	top = location['y']
	right = location['x'] + size['width']
	bottom = location['y'] + size['height']

	im = im.crop((int(left), int(top), int(right), int(bottom))) # defines crop points

	im.save(cappath)
	return cappath
