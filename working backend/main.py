# need to install requests
# type in command line: pip3 install requests
import argparse
import json
import requests
import http.client, urllib.request, urllib.parse, urllib.error, base64

# setups
api_key = "gbe55sbs99wfk9x7ab3dxq7r"

product_1_url = "https://simonguozirui.github.io/shop_right/product_1.JPG"
product_2_url = "https://simonguozirui.github.io/shop_right/product_2.JPG"
product_3_url = "https://simonguozirui.github.io/shop_right/product_3.JPG"
product_4_url = "https://simonguozirui.github.io/shop_right/product_4.JPG"
product_url = [product_1_url, product_2_url, product_3_url, product_4_url]
# code that reverse search the url and give the product number


product_1_num = 10535793
product_2_num = 10898854
product_3_num = 10898848
product_4_num = 10898852
product_num = [product_1_num, product_2_num, product_3_num, product_4_num]


def pull_product_info(product_number):
    product_url = "http://api.walmartlabs.com/v1/items/" + str(product_number) + "?apiKey=" + api_key + "&format=json"
    product_data = requests.get(product_url)
    product_json = product_data.json()
    return product_json


def get_product_info(product_number, property):
    product_json = pull_product_info(product_number)
    product_property = product_json[property]
    return product_property


def pull_reviews(product_number):
    review_url = "http://api.walmartlabs.com/v1/reviews/" + str(product_number) + "?apiKey=" + api_key + "&format=json"
    review_data = requests.get(review_url)
    review_json = review_data.json()
    return review_json


def avg_review(product_number):
    review_json = pull_reviews(product_number)
    avg_review = float(review_json['reviewStatistics']['averageOverallRating'])
    return avg_review


def review_text(product_number):
    review_json = pull_reviews(product_number)
    review_text = ''
    for x in review_json['reviews']:
        review_text += str(x['reviewText'])
    review_text = review_text.lower()
    return review_text


def getkeyphrases(product_number):
    body = {
        "documents": [
            {
                "id": "1",
                "text": review_text(product_number)
            }
        ]
    }
    # print (body["documents"][0]["text"])
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
        # print("[Errno {0}] {1}".format(e.errno, e.strerror))
        return -1
    return data


property = ["name", "salePrice", "brandName", "mediumImage"]
dict = {"name": "1", "salePrice": "2", "brandName": "3", "mediumImage": "4", "averageReview": "5", "keyPhrases": "6"}
list = [];
for i in range(len(product_num)):
    for j in range(len(property)):
        print(j)
        if 0 is j:
            dict['name'] = get_product_info(product_num[i], property[j])
        elif 1 is j:
            dict['salePrice'] = get_product_info(product_num[i], property[j])
        elif 2 is j:
            dict['brandName'] = get_product_info(product_num[i], property[j])
        elif 3 is j:
            dict['mediumImage'] = get_product_info(product_num[i], property[j])
        print(get_product_info(product_num[i], property[j]))
    dict["averageReview"] = avg_review(product_num[i])
    dict["keyPhrases"] = getkeyphrases(product_num[i])
    list.append(dict)
    dict = {}
    print(avg_review(product_num[i]))
    print(getkeyphrases(product_num[i]))
print(list)
json = json.dumps(dict)
#print(json)



    
