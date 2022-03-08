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
	r = requests.get(url)

	with open('allsubs', 'w') as f:
		f.write(r.text)


	with open('allsubs', 'r') as f:
		soup = BeautifulSoup(f.read(), 'html.parser')		
		subs = soup.find_all(id="container95m")
		i = 1
		indexall = my_dictionary()
		for sub in subs:
			try:
				title = sub.find(class_="NewsTitle").text.split(',')[0]
				langs = sub.find_all(class_="language")
				links = sub.find_all('a', class_="buttonDownload")
				for elem in links:
					strong = elem.strong.text
					if not strong.find("most"):
						links.remove(elem)
				if sub.find(title="Hearing Impaired"):
						title = "{} ¤ ".format(title)
				lang = my_dictionary()
				for language, link in zip(langs, links) :
					lang.add(language.text.replace('\n', '').split(' (')[0], link.get('href'))
				epsubs = my_dictionary()
				epsubs.add(title, lang)
				indexall.add(i, epsubs)
				i+=1

			except Exception as e: 
				pass

	print("\n[ list of subtitles Available ] : \n")
	for ind,values in indexall.items():
		print("[{0:3} ".format(ind), end=']')
		for key in values:
			print("[{0:30}".format(key), end=']')
			for lang in indexall[ind][key]:
				print("[{}".format(lang), end=']')
			print('')

	print('')
	choice = input("[ Which Sub do you want  ? ] [1-{}] : ".format(i-1))
	print('')

	if choice.isdigit():
		choice = int(choice)
	else:
		print("not number")
		exit(12)

	if choice < i:
		for value in indexall[choice] :
			ep = value
		if len(indexall[choice][ep]) == 1 :
			lang = list(indexall[choice][ep].keys())[0]
		else:
			j = 1
			for lang in indexall[choice][ep] :
				print("[{0:2} ][{1}]".format(j, lang))
				j+=1
			print('')
			lang = input("[ Which Lang do you want ? ] [1-{}]: ".format(j-1)) or "English"
			if lang.isdigit():
				if int(lang) < j:
					lang = int(lang) - 1
					lang = list(indexall[choice][ep].keys())[lang]
		try:
			link = indexall[choice][ep][lang]
		except:	
			pass
			print("\nNot good choice")
			exit(13)
		
	else:
		print("\nNot in range")
		exit(12)



	r = requests.get("https://www.addic7ed.com/{}".format(link), headers={"Referer": "https://www.addic7ed.com/"}, allow_redirects=True)

	with open('sub', 'w') as f:
		f.write(r.text)