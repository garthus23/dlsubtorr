from bs4 import BeautifulSoup
from data_process import my_dictionary

def get_tvshow_list(showlist, name):

	with open('tvlist', 'r') as f:
		soup = BeautifulSoup(f.read(), 'html.parser')
		tvshows = soup.find_all(id="qsShow")

		i = 1 
		for tvshow in tvshows:
			for show in tvshow:
				if name in show.text.lower():
					showlist.add(i, show.text.lower())
					i+=1
	return(showlist)


def get_sub_list(sublist):

	with open('allsubs', 'r') as f:
		soup = BeautifulSoup(f.read(), 'html.parser')			 
		subs = soup.find_all(id="container95m")
		i = 1
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
				sublist.add(i, epsubs)
				i+=1

			except Exception as e: 
				pass
		return (sublist)


def get_torrent_list(season, episode):

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
						print("[{0:3} ][{1}]".format(i, torrent.get('title')))
						torrentdict.add(i, torrent.get('href'))
						i=i+1
	return(torrentdict)
