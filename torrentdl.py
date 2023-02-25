import os
import re

def torrentdl(torrentdict, choice, vidname, title, name):
    
    name = re.split(r'[\ \.]', name)[0]

    os.environ["TNAME"] = vidname
    os.environ["TLINK"] = list(torrentdict.values())[choice][0]
    os.environ["SNAME"] = name.split('\'')[0]
    os.environ["SEP"] = title

    print("title={}".format(title))
    print("name={}".format(name))


    os.system('aria2c --seed-time=0 --log-level=info --summary-interval=3600 $TLINK')
    os.system('ls | grep -i "$SEP.*.mkv" | grep -i "$SNAME" | xargs -I {} mv {} ./dl/$TNAME')
