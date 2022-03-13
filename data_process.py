import requests
import os

class my_dictionary(dict):
  
    # __init__ function
    def __init__(self):
        self = dict()
    
    # Function to add key:value
    def add(self, key, value):
        self[key] = value


def html_dl(url,file):
	
	r = requests.get(url)
	with open(file, 'w') as f:
		f.write(r.text)
	return 0

def sub_dl(url,file):
	
	r = requests.get(url, headers={"Referer": "https://www.addic7ed.com/"}, allow_redirects=True)
	with open("./dl/{}".format(file), 'w') as f:
		f.write(r.text)
	return 0


def html_remove(file):
	os.remove(file)
