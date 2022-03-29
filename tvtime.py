#!/usr/bin/env python3

from data_process import *
from getpass import getpass
from bs4 import BeautifulSoup
import requests

class tvshow:
    def __init__(self, name, season, episode):
        self.name = name
        self.season = season
        self.episode = episode
        self.torrents = {} 
        self.subs = {}

    def torrentlist(self):
            with open("torrentlist", "r") as f:
                    soup = BeautifulSoup(f.read(), 'html.parser')
                    torrents = soup.find_all(class_="magnet")
                    title="S{}E{}".format(self.season, self.episode)
                    for torrent in torrents:
                        if title in torrent.get('title'):
                            if "720p" in torrent.get('title'):
                                    self.torrents[torrent.get('title')] = torrent.get('href')
            return(self.torrents)

    def version(self):
        for key in self.torrents.keys():
            print(key)

with requests.Session() as s :
    user = input('TVtime Username: ')
    pwd = getpass()
    payload = {'username': user,'password': pwd} 
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Falkon/3.2.0 Chrome/87.0.4280.144 Safari/537.36'}
    p = s.post('https://www.tvtime.com/signin', data=payload, headers ={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0'})
    r = s.get('https://www.tvtime.com/en',  headers ={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0'})
	
    with open('tvtime','w') as f:
        f.write(r.text)


with open('tvtime', 'r') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')    
    showname = soup.find_all(class_="nb-reviews-link secondary-link")
    towatch = soup.find_all(class_="episode-details poster-details")

    for show, ep in zip(showname, towatch) :
        obj = tvshow(show.text.lower(), ep.h2.a.text[1:3], ep.h2.a.text[4:])
        url = "https://eztv.ro/search/{}".format(obj.name).replace('\'', "")
        html_dl(url, "torrentlist")
        obj.torrentlist()
        print(obj.__dict__)
