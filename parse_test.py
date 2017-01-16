

def main():
	def handle_help():
		commands = ["help","\nlist categories","\npoll [i.e. Thai, Mexican, American]","\nyelp [search params]"]
		return ", ".join(commands)

	def handle_list(command):
		
		def categories():
			categories = ["Restaurants","\nSandwiches","\nNightlife","\nBars","\nFood","\nAmerican (New)","\nItalian","\nAmerican (Traditional)","\nPizza","\nChinese","\nBreakfast & Brunch","\nFast Food","\nCoffee & Tea","\nSalad","\nCafes","\nBurgers","\nSeafood","\nJapanese","\nMexican","\nDelis","\nSushi Bars","\nAsian Fusion","\nMediterranean","\nFood Trucks","\nBakeries","\nMiddle Eastern","\nFood Stands","\nPubs","\nThai"]
			return ', '.join(categories)
		
		command = command.split()
		print(command)
		if len(command) == 2:
			if command[1] == "categories":
				return categories()
		else:
			return "Fail"
	
	def handle_lunch(command):
		units = [ "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen","sixteen", "seventeen", "eighteen", "nineteen",]
		tens = ["", "", "twenty", "thirty", "forty", "fifty"]
		def text2int(item, numwords={}):
			if not numwords:	
				numwords["and"] = (1, 0)
	    		for idx, word in enumerate(units):
	    			numwords[word] = (1, idx)
				for idx, word in enumerate(tens):     
					numwords[word] = (1, idx * 10)
				current = result = 0
				
				if item not in numwords:
					raise Exception("Illegal word: " + item)
				
				scale, increment = numwords[item]
				if increment < 20:
					increment+=1
				current = current * scale + increment 
			return current

		from itertools import imap

		command = command.lower().split(" at ")
		if command < 2:
			return "Lunch is coming! Add more details (i.e. lunch at [time, [place]])"

		for item in command:
			if any(i in item for i in units):
				item = item.split()
				if len(item) > 1:
					result = ""
					for i in range(len(item)):
						if i == 0:
							result = str(text2int(item[i])) + ":"
						else:
							result += str(text2int(item[i]))
				else:
					result = str(text2int(item[0])) + ":00"
			elif any(imap(lambda c:c.isdigit(),item)):
				result = item

		return result

	command = "lunch at 1:30 at McGarvey's"
	
	if command == "help" or command == "h":
		response = handle_help()
	elif command.startswith("list"):
		response = handle_list(command)
	elif command.startswith("lunch"):
		response = handle_lunch(command)

	print response

if __name__ == '__main__':
	main()