import requests
import os
import subprocess
import json

class my_dictionary(dict):
  
    # __init__ function
    def __init__(self):
        self = dict()
    
    # Function to add key:value
    def add(self, key, value):
        self[key] = value


def html_dl(url,file):
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0', 'Connection':'close'}
    r = requests.get(url, headers=headers)
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

def torrent_duration(file):
    metadata="dl/{}".format(file)
    result = subprocess.Popen(["ffprobe", "-hide_banner", metadata],stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    for x in result.stdout.readlines():
        if "Duration" in str(x):
            return(str(x[12:23]).replace('b',''))
    return 0
