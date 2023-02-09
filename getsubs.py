#!/usr/bin/env python3

from os.path import exists
import sys
import re
from parser import *
from data_process import *
from print_input import *
from torrentdl import torrentdl


if __name__ == "__main__":

        if not exists('tvlist'):
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
        print_showlist(showlist, name)

        if season.isdigit() and episode.isdigit():
                season = int(season)
                episode = int(episode)

        namesub = input_show_choice(showlist)      
        season = "{:02d}".format(season)
        episode = "{:02d}".format(episode)
        title = "S{}E{}".format(season, episode)
        vidname = '{}_S{}E{}.mkv'.format(name, season, episode).replace(' ','_')

        url = "https://eztv.ro/search/{} {}".format(name.replace('\'',''), title)
        html_dl(url, "torrentlist")

        torrentdict = get_torrent_list(season, episode)
        print_torrentlist(torrentdict)
        torrentchoice = input_torrent_choice(torrentdict)
        
        torrentdl(torrentdict, torrentchoice, vidname, title, name)     

        print('\nVideo Duration : {}'.format(torrent_duration(vidname)))


        url = "https://www.addic7ed.com/serie/{}/{}/{}/all".format(namesub, season, episode)
        html_dl(url, "allsubs")

        indexall = my_dictionary()
        get_sub_list(indexall)
        i = print_allsub(indexall)
        link,ep = input_sub_choice(indexall, i)
 
        url="https://www.addic7ed.com/{}".format(link)
        namesub = namesub.replace('\'', '')
        ep = ep.replace('.','_')
        ver = re.split(r"\-|\ |\+|\_", ep)
         
        subname = "{}_S{}E{}.srt".format(name, season, episode).replace(' ','_')
        sub_dl(url, subname)

                                
        files = ['torrentlist', 'allsubs', 'infolist']
        for file in files:
                html_remove(file)
