# -*- coding: utf-8 -
import random

def latin(s):
	s = s[:-2]
	s = s.lower()
	s = s.replace('з','z')

	s = s.replace('а','a').replace('б','b').replace('в','v').replace('г','g')
	s = s.replace('д','d').replace('е','e').replace('ё','e').replace('ж','zh')
	s = s.replace('и','i').replace('й','i').replace('к','k').replace('л','l')
	s = s.replace('м','m').replace('н','n').replace('о','o').replace('п','p')
	s = s.replace('р','r').replace('с','s').replace('т','t').replace('у','u')
	s = s.replace('ф','ph').replace('х','h').replace('ц','c').replace('ч','ch')
	s = s.replace('ш','sh').replace('щ','sch').replace('ъ','').replace('ы','y')
	s = s.replace('ь','').replace('э','e').replace('ю','iu').replace('я','ia')
	return s
def getNAME():
	path = '/home/fanat_tortov/Документы/selenium/names/'

	f = open(path+'counter','r')
	count = f.read().split('\n')
	f.close()

	f = open(path+'rus_name','r')
	names = f.read().split('\n')
	f.close()

	f = open(path+'rus_surname','r')
	surnames = f.read().split('\n')
	f.close()

	n_r = random.randint(1,int(count[0]))
	s_r = random.randint(1,int(count[1]))
	s = ""

	for i in surnames:
		s_r = s_r-int(i.split(' ')[-1])
		if (s_r<=0):
			s = ' '.join(i.split(' ')[:-1])+' '
			break

	for i in names:
		n_r = n_r-int(i.split(' ')[-1])
		if (n_r<=0):
			s += ' '.join(i.split(' ')[:-1])
			break


	data = '%04d.%02d.%02d' % (random.randint(1970,2000),random.randint(1,12),random.randint(1,28))
	NAME = s+' '+latin(s)+" "+data
	return NAME
#return NAME