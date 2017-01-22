#need to install requests
#type in command line: pip3 install requests
import json
import requests
import http.client, urllib.request, urllib.parse, urllib.error, base64
#setups
api_key = "gbe55sbs99wfk9x7ab3dxq7r"
product_num = 12417832

#import from phone



def product():
	product_url = "http://api.walmartlabs.com/v1/items/" + str(product_num) + "?apiKey=" + api_key + "&format=json"
	product_data = requests.get(product_url)
	print (product_data.json())

def get_reviews():
	review_url = "http://api.walmartlabs.com/v1/reviews/" + str(product_num) + "?apiKey=" + api_key + "&format=json"
	review_data = requests.get(review_url)
	review_json = review_data.json()
	return review_json


def avg_review():
	review_json = get_reviews()
	avg_review = float(review_json['reviewStatistics']['averageOverallRating'])
	return avg_review

def review_text():
	review_json = get_reviews()
	review_text = ''
	for x in review_json['reviews']:
		review_text += str(x['reviewText'])
	review_text = review_text.lower()
	return review_text

def getkeyphrases():
	
    body = {
        "documents": [
            {
                "id": "1",
                "text": review_text()
            }
        ]
    }


    #print (body["documents"][0]["text"])
    # Request headers
    headers = {'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': 'c558677e0f9245598fc466f7eb0989b7'}
    # Request parameters
    params = urllib.parse.urlencode({'numberOfLanguagesToDetect': '{1}'})

    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/text/analytics/v2.0/keyPhrases?%s" % params, str(body), headers)
        response = conn.getresponse()
        data = json.loads(response.read().decode())["documents"][0]["keyPhrases"]
        conn.close()
        return data


    except Exception as e:
        #print("[Errno {0}] {1}".format(e.errno, e.strerror))
    	return -1
    return data

#product()
#print (avg_review())
#print (review_text())
print (getkeyphrases())



