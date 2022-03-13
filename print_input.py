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

def input_sub_choice(allsub, i):

		choice = input("\n[ Which Sub do you want	? ] [1-{}] : ".format(i-1))
		print('')

		if choice.isdigit():
			choice = int(choice)
		else:
			print("not number")
			exit(12)

		if choice < i:
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

	choice = input("\n[ Choose a torrent ] [1-{}] : ".format(len(torrentdict)))

	if choice.isdigit() and int(choice) <= len(torrentdict):
		choice = int(choice)
	else:
		print('Not a good choice')
		exit(13)

	return (choice)
