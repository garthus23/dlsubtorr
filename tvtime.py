#!/usr/bin/env python3

from getpass import getpass
import requests


with requests.Session() as s :

	user = input('TVtime Username: ')
	pwd = getpass()
	payload = {'username': user,'password': pwd} 
	headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Falkon/3.2.0 Chrome/87.0.4280.144 Safari/537.36'}

	p = s.post('https://www.tvtime.com/signin', data=payload, headers ={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0'})
	r = s.get('https://www.tvtime.com/en', headers ={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0'})

	with open('test','w') as file:
		file.write(r.text)
