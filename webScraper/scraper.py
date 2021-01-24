import requests
from bs4 import BeautifulSoup as bs
import re

search = input("\n\n\033[1mWhat game are you looking for a sale on?\033[0m \n")

def game_sale_search(search):
	search = search.replace(" ", "_").replace("'", "%27")

	url = "https://store.steampowered.com/search/?term=" + search
	page = requests.get(url)
	soup = bs(page.content, "html.parser")
	found_games = soup.find_all("a", class_="search_result_row")

	first_result = found_games

	try:
		first_result = found_games[0]
	except:
		search_again = input("I couldn't find a game of that name.  Wanna try again?\n")
		game_sale_search(search_again)


	# FIRST RESULT
	FR_title = first_result.find("span", class_="title").text
	FR_link = re.findall("href=\"[^ ]*\"", str(first_result))
	FR_link = str(FR_link)[8:-3]

	FR_percent_discount = first_result.find("div", class_="col search_discount responsive_secondrow").text.strip()

	if FR_percent_discount == "":
		FR_original_price = first_result.find("div", class_="col search_price responsive_secondrow").text.strip()
		if FR_original_price == "Free to Play":
			print("\n\nWhat are you doing!? " + str(FR_title) + " is \033[92mFree To Play\033[0m! \nGet it here: \033[4m" + FR_link + "\033[0m\n\n")
		else:
			print("\n\n"+("\033[91m" + FR_title + "\033[0m").strip(), end=" ")
			print("is not on sale.")
			print("It's normal price is currently " + FR_original_price + ".\n\n")
	else:
		FR_original_price = first_result.find("div", class_="col search_price discounted responsive_secondrow").find("span").text.strip()
		FR_discounted_price = first_result.find("div", class_="col search_price discounted responsive_secondrow").text.strip().replace(FR_original_price, "")
		print("\n\n"+("\033[92m" + FR_title + "\033[0m").strip(), end=" ")
		print("is on sale!\nIt's normal price was " + FR_original_price +", but it is now \033[1m" + FR_percent_discount[1:] + "\033[0m off bringing the total to \033[92m" + FR_discounted_price + "\033[0m!")
		print("Get it here: \033[4m" + FR_link + "\033[0m\n\n")


	satisfactory = input("Was this the game that you were looking for? (y/n) ")
	negative = ["n", "no", "nah", "nope"]
	positive =["y" ,"ya", "yes", "yeah"]

	if satisfactory.lower() in negative:
		input("Dang. Was it any of these? Type in the name of the game from this list that interests you. [enter to show list]")
		for game in found_games:
			print(game.find("span", class_="title").text + "\n")
		search = input("\n\nWhich are you looking for a sale on? \n")
		game_sale_search(search)
	elif satisfactory.lower() in positive:
		print("Great! See ya.")
		return
	else:
		print("I have no idea what you just said!  Imma head out now.")
		return


game_sale_search(search)
