#!/usr/bin/env python3

from getpass import getpass
from bs4 import BeautifulSoup
import requests



################### get data from tvtime ######################

with requests.Session() as s :

	user = input('TVtime Username: ')
	pwd = getpass()
	payload = {'username': user,'password': pwd} 
	headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Falkon/3.2.0 Chrome/87.0.4280.144 Safari/537.36'}

	p = s.post('https://www.tvtime.com/signin', data=payload, headers ={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0'})
	r = s.get('https://www.tvtime.com/en',  headers ={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0'})
	print (r.status_code)
	with open('tvtime','w') as f:
		f.write(r.text)


###### retrieve episode towatch list ##############


with open('tvtime', 'r') as f:
	soup = BeautifulSoup(f.read(), 'html.parser')    
	showname = soup.find_all(class_="nb-reviews-link secondary-link")
	towatch = soup.find_all(class_="episode-details poster-details")


	for show, ep in zip(showname, towatch) :
		print(show.text)
		print(ep.h2.a.text)
		print('-----------')
