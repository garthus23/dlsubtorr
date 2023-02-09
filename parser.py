from bs4 import BeautifulSoup
from data_process import *

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
                                title = sub.find(class_="NewsTitle").text#.split(',')[0].replace('Version ', '')
                                langs = sub.find_all(class_="language")
                                links = sub.find_all('a', class_="buttonDownload")
                                news = sub.find_all('td', class_="newsDate")
                                for elem in links:
                                        strong = elem.strong.text
                                        if not strong.find("most"):
                                                links.remove(elem)
                                if sub.find(title="Hearing Impaired"):
                                        title = "{} HI ".format(title)
                                lang = my_dictionary()
                                for language, link in zip(langs, links) :
                                        lang.add(language.text.replace('\n', '').split(' (')[0], link.get('href'))
                                epsubs = my_dictionary()
                                epsubs.add(title, lang)
                                epsubs.add('news', news[0].text.replace('\t','').replace('\n',''))
                                for key, value in lang.items():
                                    if key == 'English' or key == 'French':
                                        sublist.add(i, epsubs)
                                i+=1

                        except Exception as e: 
                                pass
                return (sublist)


def get_torrent_list(season, episode):

        with open("torrentlist", "r") as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                torrents = soup.find_all(class_="magnet")
                infos = soup.find_all('a', class_="epinfo")
                torrentdict = my_dictionary()
                                 
                print('')
                title="S{}E{}".format(season, episode)
                for torrent,ep in zip(torrents,infos) :
                        if title in torrent.get('title'): 
                                if "720p" in torrent.get('title') or "1080p" in torrent.get('title'):
                                    if len(torrent.get('title')) > 2:
                                        info= [torrent.get('href'), ep.get('href')]
                                        torrentdict.add(torrent.get('title'), info)
                for key, value in torrentdict.items():
                    url="https://eztv1.xyz{}".format(value[1])
                    html_dl(url, "infolist")
                    with open("infolist", "r") as f:
                        soup = BeautifulSoup(f.read(), 'html.parser')
                        seed = soup.find_all('span', class_="stat_red")
                        value.append(seed[0].text)
        return(torrentdict)
