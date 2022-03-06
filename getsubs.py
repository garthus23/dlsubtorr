#!/usr/bin/python3

from bs4 import BeautifulSoup
import requests
import sys



class my_dictionary(dict):
  
    # __init__ function
    def __init__(self):
        self = dict()
          
    # Function to add key:value
    def add(self, key, value):
        self[key] = value




if __name__ == "__main__":

	if len(sys.argv) == 4 :
		name = sys.argv[1]
		season = sys.argv[2]
		episode = sys.argv[3]

	else:
		exit(0)
			
	url = "https://www.addic7ed.com/serie/{}/{}/{}/all".format(name, season, episode)	
	print(url)
	r = requests.get(url)

	with open('allsubs', 'w') as f:
		f.write(r.text)


	with open('allsubs', 'r') as f:
		soup = BeautifulSoup(f.read(), 'html.parser')		
#		print(soup)
		subs = soup.find_all(id="container95m")


#		print(subs)		
		for sub in subs:
			try:
				title = sub.find(class_="NewsTitle").text
				print(title)
				langs = sub.find_all(class_="language")
				links = sub.find_all('a', class_="buttonDownload")
#				for language in alllang:
#					print(language.text)
				lang = my_dictionary()
				for language, link in zip(langs, links) :
#					print(language.text.replace('\n',''))
#					print('~~~~~~~')
#					print(link.get('href'))
					lang.add(language.text.replace('\n', ''), link.get('href'))
				print(lang)
					

				print("----------------------------------------------")
			except Exception as e: 
				print(e)


#r = requests.get("https://www.addic7ed.com/original/139326/1", headers={"Referer": "https://www.addic7ed.com/"}, allow_redirects=True)

#with open('url', 'w') as f:
#	f.write(r.text)
#	f.close()
