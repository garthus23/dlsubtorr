import os
import re

def torrentdl(torrentdict, choice, vidname, title, name):
	
	name = re.split(r'[\ \.]', name)[0]

	os.environ["TNAME"] = vidname
	os.environ["TLINK"] = torrentdict[choice]               
	os.environ["SNAME"] = name
	os.environ["SEP"] = title


	os.system('aria2c --seed-time=0  --log-level=info --summary-interval=3600 $TLINK')
	os.system('ls | grep -i "$SEP.*.mkv" | grep -i "$SNAME" | xargs -I {} mv {} ./dl/$TNAME')
