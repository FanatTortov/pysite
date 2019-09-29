# -*- coding: utf-8 -
import sys
import time
import re
import requests

sys.path.insert(1, '/home/fanat_tortov/Документы/selenium')
from module import *

def getProxL(raw_str):
	js_expRaw = re.findall(r'<\/table><script type=\"text\/javascript\">[^>]+>', raw_str)
	js_exp = ''
	if len(js_expRaw) > 0:
		js_exp = re.sub(r'<[^>]+>', '', js_expRaw[0], count=0)
	js_var = {}
	exec(js_exp, js_var)

	proxy_list = []
	items = re.findall(r'<font class=spy14>(?:[\d]+\.)+(?:[^>]+>){4}', raw_str)

	for s in items:
		proxy = re.sub(r'<[^>]+>', '', s, count=0)
		js_port_exp = re.findall(r'\+\([^\)]+\)', proxy)
		proxy = re.findall(r'(?:[\d]+\.)+[\d]+', proxy)[0]
		port = ''
		for i in js_port_exp:
			port+=str(eval(i[1:], js_var))
		proxy_list.append(proxy+":"+port)
	return proxy_list


def thrds(array):
	prox = ProxyManager()
	k = 40
	threads=[]
	counter = 0
	while len(array) > counter:
		if len(threads)<k:
			new_thread = threading.Thread(target=prox._threadProxy, args=(array[counter], 10, True))
			threads.append(new_thread)
			new_thread.start()
			counter+=1
			if counter%100==1:
				print("Count check proxy:"+str(len(prox.prox_arr)))
		for i in threads:
			if not i.isAlive():
				threads.remove(i)
		time.sleep(0.1)
	print("Count all check proxy:"+str(len(prox.prox_arr)))
	if len(threads) > 0:
		time.sleep(30)
	for i in threads:
		i.do_run = False
	return True



if __name__ == "__main__":
	r = requests.post("http://spys.one/proxies/")

	raw_str = r.text.encode('utf8')

	get_cookies = re.findall(r'<input type=\'hidden\' name=\'xf0\'[^>]+>', raw_str)
	cookies = re.search(r'value=\'(.*)\'>', get_cookies[0], re.IGNORECASE).group(1)


	#					4		2		3		2
	data={'xpp':5, 'xf1':0, 'xf2':0, 'xf4':0, 'xf5':0}
	data['xf0']=cookies
	c0 = 0
	proxy_list = []
	for c1 in range(4):
		for c2 in range(2):
			for c3 in range(3):
				for c4 in range(2):
					c0+=1
					data['xf1']=c1
					data['xf2']=c2
					data['xf4']=c3
					data['xf5']=c4
					print("Search N:"+str(c0)+" of "+str(4*2*3*2))
					raw_str = requests.post("http://spys.one/proxies/", data).text.encode('utf8')
					proxy_list += getProxL(raw_str)
	print('Count all proxy:'+str(len(proxy_list)))
	proxy_list = list(set(proxy_list))
	print('Count sorted proxy:'+str(len(proxy_list)))
	thrds(proxy_list)

	#######

	print("Successfull")
