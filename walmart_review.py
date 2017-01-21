#need to install requests
#type in command line: pip3 install requests
import json
import requests
#setups
api_key = "gbe55sbs99wfk9x7ab3dxq7r"
product_num = 12417832

def product():
	product_url = "http://api.walmartlabs.com/v1/items/" + str(product_num) + "?apiKey=" + api_key + "&format=json"
	product_data = requests.get(product_url)
	print (product_data.json())

def reviews():
	review_url = "http://api.walmartlabs.com/v1/reviews/" + str(product_num) + "?apiKey=" + api_key + "&format=json"
	reviews_data = requests.get(review_url)
	print (reviews_data.json())

#product()
reviews()


