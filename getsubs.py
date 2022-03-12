#!/usr/bin/python3

from bs4 import BeautifulSoup
import requests
import sys
import os



class my_dictionary(dict):
  
    # __init__ function
    def __init__(self):
        self = dict()
          
    # Function to add key:value
    def add(self, key, value):
        self[key] = value




if __name__ == "__main__":

	url = "https://www.addic7ed.com"
	r = requests.get(url)
	
	with open('tvlist', 'w') as f:
		f.write(r.text)

	if len(sys.argv) == 4 :
		name = sys.argv[1]
		season = sys.argv[2]
		episode = sys.argv[3]

	else:
		name = input("Show Title : ").lower()
		season = input("Season : ")
		episode = input("Episode : ")

	with open('tvlist', 'r') as f:
		soup = BeautifulSoup(f.read(), 'html.parser')
		tvshows = soup.find_all(id="qsShow")
		showlist=my_dictionary()

		i = 1
		for tvshow in tvshows:
			for show in tvshow:
				if name in show.text.lower():
					showlist.add(i, show.text.lower())
					i+=1

	if i == 0:
		print("No TvShow Found")
		exit(12)

	print('')
	for key, value in showlist.items():
		if name in value :
			print("[{0:3} ] [{1}]".format(key, value))

	if len(showlist) == 1:
		name = showlist[1]
	else:
		choice = input("\nChoose a TvShow [0:{}] : ".format(len(showlist)))
		if choice.isdigit() and int(choice) < len(showlist):
			choice = int(choice)
		else:
			print("Err : Not a Digit or not in range")
			exit(12)

		name = showlist[choice]
		
	if season.isdigit() and episode.isdigit():
		season = int(season)
		episode = int(episode)

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
				title = sub.find(class_="NewsTitle").text.split(',')[0].replace('Version ', '')
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

	count = 0
	print("\n[ list of subtitles Available ] : \n")
	for ind,values in indexall.items():
		print("[{0:3} ".format(ind), end=']')
		for key in values:
			print("[{0:30}".format(key), end=']')
			for lang in indexall[ind][key]:
				print("[{}".format(lang), end=']')
				count+=1
			print('')
	if count == 0:
		print("no Subs Found, Season or Episode out of range")
		exit(23)

	choice = input("\n[ Which Sub do you want  ? ] [1-{}] : ".format(i-1))
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

	name = name.replace('\'', '')	
	subname = "{}_S{:02d}E{:02d}_{}.srt".format(name, season, episode, ep).replace(' ','_')
	with open(subname, 'w') as f:
		f.write(r.text)



	season = "{:02d}".format(season)
	episode = "{:02d}".format(episode)

	url = "https://eztv.ro/search/{}".format(name)
	r = requests.get(url)

	with open("torrentlist", 'w') as f:
		f.write(r.text)

	with open("torrentlist", "r") as f:
		soup = BeautifulSoup(f.read(), 'html.parser')
		torrents = soup.find_all(class_="magnet")
		torrentdict = my_dictionary()
		
		print('')
		i = 1
		title="S{}E{}".format(season, episode)
		for torrent in torrents :
			if title in torrent.get('title'):
				if "720p" in torrent.get('title') or "1080p" in torrent.get('title'):
					torrentdict.add(i, torrent.get('href'))
					print("[{0:3} ][{1}]".format(i, torrent.get('title')))
					i+=1

	choice = input("\n[ Choose a torrent ] [1-{}] : ".format(i-1))

	if choice.isdigit() and int(choice) < i:
			choice = int(choice)
	else:
		print('Not a good choice MF')
		exit(13)
		
	vidname = '{}_S{}E{}_{}.mkv'.format(name, season, episode, ep).replace(' ','_')
		
	os.environ["TNAME"] = vidname
	os.environ["TLINK"] = torrentdict[choice]		
	os.environ["SEP"] = title
		
	os.system('aria2c --seed-time=0  $TLINK')
	os.system('ls | grep $SEP | xargs -I {} mv {} $TNAME')
	
	os.remove("torrentlist")
	os.remove("allsubs")
	os.remove("tvlist")
