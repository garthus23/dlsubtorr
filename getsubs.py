#!/usr/bin/python3

import sys
from bs4 import BeautifulSoup
from parser import *
from data_process import *
from print_input import *
from torrentdl import torrentdl


if __name__ == "__main__":

	html_dl("https://www.addic7ed.com", "tvlist")

	if len(sys.argv) == 4 :
		name = sys.argv[1]
		season = sys.argv[2]
		episode = sys.argv[3]
	else:
		name = input("Show Title : ").lower()
		season = input("Season : ")
		episode = input("Episode : ")
	
	showlist = my_dictionary()
	get_tvshow_list(showlist, name)

	if len(showlist) == 0:
		print("No TvShow Found")
		exit(12)

	print('')
	for key, value in showlist.items():
		if name in value :
			print("[{0:3} ] [{1}]".format(key, value))

	if len(showlist) == 1:
		name = showlist[1]
	else:
		choice = input("\nChoose a TvShow [1:{}] : ".format(len(showlist)))
		if choice.isdigit() and int(choice) <= len(showlist):
			choice = int(choice)
		else:
			print("Err : Not a Digit or not in range")
			exit(12)

		name = showlist[choice]
	if season.isdigit() and episode.isdigit():
		season = int(season)
		episode = int(episode)

	url = "https://www.addic7ed.com/serie/{}/{}/{}/all".format(name, season, episode)
	html_dl(url, "allsubs")

	indexall = my_dictionary()
	get_sub_list(indexall)
	i = print_allsub(indexall)
	link,ep = input_sub_choice(indexall, i)

	r = requests.get("https://www.addic7ed.com/{}".format(link), headers={"Referer": "https://www.addic7ed.com/"}, allow_redirects=True)
	url="https://www.addic7ed.com/{}".format(link)
	name = name.replace('\'', '')
	ep = ep.replace('.','_')

	subname = "{}_S{:02d}E{:02d}_{}.srt".format(name, season, episode, ep).replace(' ','_')
	sub_dl(url, subname)

	season = "{:02d}".format(season)
	episode = "{:02d}".format(episode)
	title = "S{}E{}".format(season, episode)
	vidname = '{}_S{}E{}_{}.mkv'.format(name, season, episode, ep).replace(' ','_')

	url = "https://eztv.ro/search/{}".format(name)
	html_dl(url, "torrentlist")

	torrentdict = get_torrent_list(season, episode)
	torrentchoice = input_torrent_choice(torrentdict)
	
	torrentdl(torrentdict, torrentchoice, vidname, title, name)	
			
	files = ['torrentlist', 'allsubs', 'tvlist']
	for file in files:
		html_remove(file)
