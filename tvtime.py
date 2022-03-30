#!/usr/bin/env python3

from data_process import *
import time
from getpass import getpass
from bs4 import BeautifulSoup
import requests
import re

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
            version = ["720p", "1080p"]
            for torrent in torrents:
                if title in torrent.get('title'):
                    for ver in version :
                        if ver in torrent.get('title'):
                            self.torrents[torrent.get('title').lower()] = torrent.get('href')
            return(self.torrents)

    def sublist(self):
        with open("sublist", "r") as f:
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
                        continue
                    for language, link in zip(langs, links) :
                        if language.text.replace('\n', '').split(' (')[0] == 'English':
                            self.subs[title.lower()] =  link.get('href')
                except Exception as e:
                    pass
        return (self.subs)

    def dlsubtorr(self):
        for key in self.torrents.keys():
            for version in self.subs.keys():
                verlist = re.split('\'|\.|\-|\ |\+|720|1080', version)
                for ver in verlist :
                    if ver in key and len(ver) > 2:
                        name = re.sub('[\ \'\-]', '_', self.name)
                        filename = "{}_S{}E{}_{}.srt".format(name, self.season, self.episode, ver)
                        url = "https://www.addic7ed.com/{}".format(self.subs[version])
                        sub_dl(url,filename)
                        
                        os.environ["SNAME"] = name.split('_')[0]
                        os.environ["SEP"] = "S{}E{}".format(self.season, self.episode)
                        os.environ["TNAME"] = "{}_S{}E{}_{}.mkv".format(name, self.season, self.episode, ver) 
                        os.environ["TLINK"] = self.torrents[key]
                        os.system('aria2c --seed-time=0  --log-level=info --summary-interval=3600 $TLINK')
                        os.system('ls | grep -i "$SEP.*.mkv" | grep -i "$SNAME" | xargs -I {} mv {} ./dl/$TNAME')
                        return(0)

    def checkdl(self):

        name = re.sub('[\ \'\-]', '_', self.name)
        sep = "S{}E{}".format(self.season, self.episode)
        for filename in os.listdir('./dl/'):
            if name in filename:
                if sep in filename:
                    print("file {} S{}E{} already downloaded".format(self.name, self.season, self.episode))
                    return(1)
        return(0)
            

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
        if obj.checkdl() == 1 :
            continue
        url = "https://eztv.ro/search/{}".format(obj.name).replace('\'', "")
        html_dl(url, "torrentlist")
        obj.torrentlist()
        url = "https://www.addic7ed.com/serie/{}/{}/{}/all".format(obj.name, obj.season, obj.episode)
        html_dl(url, "sublist")
        obj.sublist()
        obj.dlsubtorr()
