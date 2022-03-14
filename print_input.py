def print_allsub(subdict):

	count = 0 
	print("\n[ list of subtitles Available ] : \n")
	for ind,values in subdict.items():
		print("[{0:3} ".format(ind), end=']')
		for key in values:
			print("[{0:30}".format(key), end=']')
			for lang in subdict[ind][key]:
				print("[{}".format(lang), end=']')
				count+=1
			print('')
	if count == 0:
		print("no Subs Found, Season or Episode out of range")
		exit(23)
	
	return(count)

def print_showlist(showdict, name):

	if len(showdict) == 0:
		print("No TvShow Found")
		exit(12)

	print('')
	for key, value in showdict.items():
		if name in value :
			print("[{0:3} ] [{1}]".format(key, value))
	return (0)

def print_torrentlist(torrentdict):

	if len(torrentdict) == 0:
		print("No torrent Found")
		exit(12)
	i = 1
	for key in torrentdict.keys():
		print("[{0:3} ] [{1}]".format(i,key))
		i+=1

	return(0)



def input_show_choice(showdict):

	if len(showdict) == 1:
		return (showdict[1])
	else:
		choice = input("\nChoose a TvShow [1:{}] : ".format(len(showdict)))
		if choice.isdigit() and int(choice) <= len(showdict):
			choice = int(choice)
		else:
			print("Err : Not a Digit or not in range")
			exit(12)

		return(showdict[choice])



def input_sub_choice(allsub, i):


		choice = input("\n[ Which Sub do you want	? ] [1-{}] : ".format(i))
		print('')

		if choice.isdigit():
			choice = int(choice)
		else:
			print("not number")
			exit(12)

		if choice <= i:
			for value in allsub[choice] :
				ep = value
			if len(allsub[choice][ep]) == 1 :
				lang = list(allsub[choice][ep].keys())[0]
			else:
				j = 1
				for lang in allsub[choice][ep] :
					print("[{0:2} ][{1}]".format(j, lang))
					j+=1
				print('')
				lang = input("[ Which Lang do you want ? ] [1-{}]: ".format(j-1)) or "English"
				if lang.isdigit():
					if int(lang) < j:
						lang = int(lang) - 1
						lang = list(allsub[choice][ep].keys())[lang]
			try:
				link = allsub[choice][ep][lang]
			except: 
				pass
				print("\nNot good choice")
				exit(13)
			 
		else:
			print("\nNot in range")
			exit(12)

		return (link, ep)

def input_torrent_choice(torrentdict):
	
	if len(torrentdict) == 1:
		return (0)

	choice = input("\n[ Choose a torrent ] [1-{}] : ".format(len(torrentdict)))

	if choice.isdigit() and int(choice) <= len(torrentdict) + 1:
		choice = int(choice)
	else:
		print('Not a good choice')
		exit(13)

	return (choice-1)
