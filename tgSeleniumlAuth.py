# -*- coding: utf-8 -
import os
import random
import time
import re
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import sys
from PIL import Image
from io import BytesIO
from sys import version_info
import signal
import requests
from contextlib import contextmanager
import pickle
import tgappmanage

from module import *
		

def checkLoad(brow):
	return brow.finds_by_class('login_form_wrap') != False

def getCode(brow):
	code = tgappmanage.getCode(wait=1)
	brow.maxWin()
	return code

def getLastMessage(brow):
	el = brow.finds_by_class('im_history_message_wrap',-1)
	return el.text if (el) else ''

def getDialogName(brow,click=False):
	div = brow.finds_by_class('nav-pills',0)
	li = brow.finds_by_tag(div,'li',0)
	diag = brow.finds_by_class(li,'im_dialog_message_wrap',0)
	if (click):
		return brow.click(diag)
	name_d = brow.finds_by_tag(diag,"span",0)
	return name_d.text

def selTgChat(brow):
	searchElem = brow.finds_by_class('im_dialogs_search_field',0)
	brow.send_keys(searchElem,"Telegram")
	while (getDialogName(brow)!="Telegram"):
		time.sleep(0.2)
	return getDialogName(brow,True)

def getBrowActivCode(brow,isNumb=True):
	selTgChat(brow)
	answ = getLastMessage(brow)
	if answ=="":
		return None
	if (isNumb):
		match = re.findall(r'\d+',answ)
		if len(match)>0 and len(match[-1])==5:
			return match[-1]
		else:
			return None
	else:
		s = answ.split('\n')
		for i in s:
			if(re.search(r'my.telegram.org',i) is not None):
				return (s[s.index(i)+1])
		else:
			return None

def getApi(brow):
	brow.mainHandle = brow.brow.current_window_handle
	brow.brow.execute_script("window.open('https://my.telegram.org');")
	handles = brow.brow.window_handles.copy()
	if (len(handles)>1):
		handles.remove(brow.mainHandle)
	else:
		return None
	brow.brow.switch_to_window(handles[0])
	if (re.search(r'my\.telegram\.org',brow.brow.current_url) is None):
		return None
	else:
		phoneForm = brow.find_by_id('my_login_phone')
		if (not phoneForm):
			return None
		else:
			brow.send_keys(phoneForm,''.join(brow.user.number()))
			brow.click_by_class(brow.find_by_id('my_send_form'),'btn-lg')
			brow.brow.switch_to_window(brow.mainHandle)
			if (not brow.getSite(brow.brow.current_url)):
				return None
			else:
				code = getBrowActivCode(brow,False)
				if (code is None):
					return None
				else:
					brow.brow.switch_to_window(handles[0])
					#Place for EMAIL SYNC
					codeForm = brow.find_by_id('my_password')
					brow.send_keys(codeForm,code)
					brow.click_by_class(brow.find_by_id('my_login_form'),'btn-lg')
					while (brow.find_by_id('my_login_form')):
						time.sleep(0.2)
					else:
						for i in brow.finds_by_tag('a'):
							if (i.get_attribute('href')=="https://my.telegram.org/apps"):
								brow.click(i)
								break
						if (brow.finds_by_name('app_platform')):
							brow.send_keys(brow.find_by_id('app_title'),brow.user.person.getTitle())
							brow.send_keys(brow.find_by_id('app_shortname'),brow.user.person.shortName)
							radio = brow.finds_by_name('app_platform')
							brow.click(brow.finds_by_name('app_platform',random.randint(0,len(radio)-1)))
							brow.click_by_id('app_save_btn')
						if (not brow.find_by_id('app_edit_form')):
							return None
						appidEls = brow.finds_by_class('uneditable-input')
						brow.user.appId = appidEls[0].text
						brow.user.appHash = appidEls[1].text
						#Place for EMAIL SYNC
						brow.brow.close()
						brow.brow.switch_to_window(brow.mainHandle)
						return True


def tgAuth(brow):
	if (not brow.init()):
		return False
	country,number=brow.user.number()
	cntr = brow.finds_by_name('phone_country',0)
	if (cntr):
		brow.click(cntr)
		brow.send_keys(cntr,country)
		nbr = brow.finds_by_name('phone_number',0)
		brow.click(nbr)
		brow.send_keys(nbr,number)
		brow.click_by_class('login_head_submit_btn')
		time.sleep(0.5)
		brow.click_by_class('btn-md-primary')
		cdEl = False
		for i in range(3):
			cdEl = brow.finds_by_name('phone_code',0)
		if (cdEl):
			brow.click(cdEl)
			code = getCode(brow)
			brow.send_keys(cdEl,code)

			pwdinp = brow.finds_by_name('password',0)
			if (pwdinp):
				brow.click(pwdinp)
				pwd = getPass(country+number)
				brow.send_keys(pwdinp,pwd)
				brow.click_by_class('login_head_submit_btn')
			if (brow.finds_by_class('im_dialogs_search_field',0) and (not brow.finds_by_name('phone_code',0))):
				print("Congrat")
				return True
			else:
				return False
				#WRITE SEARCH TG ACC
			# brow.user.link = 
			# brow.getSite('https://web.telegram.org/#/im?p=@telegram')

		else:
			print("Eror to connect")
			return False
def nextACC():
	pass

def apiUse(user):
	user.getBrowCode = lambda:getBrowActivCode(user.brow)
	user.telethon = TelethonWorker(user.appId,user.appHash,"".join(user.number),self.user.proxy_man.proxy['proxy'],user.getBrowCode)
	#try except


def tgOpen(user):
	tg = user
	tg.brow.minWin()
	tg.smsWork = Sim5Worker()
	if (tg.smsWork.buyNumber()):
		cntr = tg.smsWork.tgCountry
		nmbr = tg.smsWork.tgPhone
	else:
		return False
	tg.number([cntr,nmbr])
	if (tgappmanage.tgWork(cntr,nmbr,tg.proxy_man.proxy['proxy'],tg.smsWork)):
		if (tgAuth(tg.brow)):
			tg.brow.maxWin()
			print("Done")
			if (getApi(tg.brow) is None):
				print("Error")
			else:
				apiUse(tg)
	else:
		nextACC()
	while (True):
		print('Script done, i`m wait')
		time.sleep(15)



if __name__ == "__main__":
	link = 'https://web.telegram.org'
	tg = User(link,checkLoad,hide=False)
	new_thread1 = threading.Thread(target=tgOpen, args=(tg,))
	new_thread1.start()
