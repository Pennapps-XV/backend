# need to install requests
# type in command line: pip3 install requests
import argparse
import json
import requests
from collections import Counter
import http.client, urllib.request, urllib.parse, urllib.error, base64

# setups
api_key = "gbe55sbs99wfk9x7ab3dxq7r"

product_1_url = "http://45.33.95.66/product_1.JPG"
product_2_url = "http://45.33.95.66/product_2.JPG"
product_3_url = "http://45.33.95.66/product_3.JPG"
product_4_url = "http://45.33.95.66/product_4.JPG"
product_url = [product_1_url, product_2_url, product_3_url, product_4_url]

def removes(yes):
    no = ["Walmart.com", ".", ","]
    for x in no:
        yes = yes.replace(x, '')
    return yes.upper()

def post_some_dict(dict):
    headers = {'Content-type': 'application/json'}
    r = requests.post("http://127.0.0.1:5000/search", data=json.dumps(dict), headers=headers)
    #print(r.text)
    return r.text

def parse_image(image):
    out = json.loads(post_some_dict({"image_url": image}))['titles']
    #print(out)
    #out = [x for x in out if 'walmart' in x]
    threshold = 2
    #out = [x[27:-9] for x in out]
    #print(out)
    large = []
    for line in out:
        line = line.replace('-', '')
        line = removes(line)
        line = line.split(' ')
        #print(line)
        for word in line:
            large.append(word)
    #print(large)
    c = Counter(large).most_common()

    keywords = []

    for x in c:
        if x[1] > threshold:
            keywords.append(x[0])
    #print(keywords)
    return ' '.join(keywords)

def parse_wallmart(keywords):
    #print(keywords)
    outa = json.loads(requests.get("http://api.walmartlabs.com/v1/search?apiKey=frt6ajvkqm4aexwjksrukrey&query=" + keywords + "&format=json").text)
    #print(outa)
    #outa['items'][0]['name'][0]
    try:
        item_id = outa['items'][0]['itemId']
    except:
        item_id = 000000
    return item_id


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
    try:
        avg_review = float(review_json['reviewStatistics']['averageOverallRating'])
    except: avg_review = 0.0
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

def pprint(lis):
    from tabulate import tabulate
    print(tabulate(lis, headers=['name', 'price', 'brand', 'reviews', 'phrases']))

property = ["name", "salePrice", "brandName", "mediumImage"]
dicts = {"name": "1", "salePrice": "2", "brandName": "3", "mediumImage": "4", "averageReview": "5", "keyPhrases": "6"}
dict = []
list = []
print("Processing")
lists = []
for i in range(len(product_num)):
    product_num[i] = parse_wallmart(parse_image(product_url[i]))
    for j in range(len(property)):
        #print(j)
        if product_num[i] != 000000:
            if 0 is j:
                o = get_product_info(product_num[i], property[j])
                dict.append(o)
                dicts['name'] = o
            elif 1 is j:
                o = get_product_info(product_num[i], property[j])
                dict.append(o)
                dicts['salePrice'] = o
            elif 2 is j:
                o = get_product_info(product_num[i], property[j])
                dict.append(o)
                dicts['brandName'] = o
            elif 3 is j:
                o = get_product_info(product_num[i], property[j])
                dicts['mediumImage'] = o
            #print(get_product_info(product_num[i], property[j]))
    if product_num[i] != 000000:
        o = avg_review(product_num[i])
        dict.append(o)
        dicts['averageReview'] = o
        o = getkeyphrases(product_num[i])
        dict.append(o)
        dicts['keyPhrases'] = o
        list.append(dict)
        lists.append(dicts)
        dict = []
        dicts = {}
        #print(avg_review(product_num[i]))
        #print(getkeyphrases(product_num[i]))
    else:
        #print("Product not found")
        pass
pprint(list)
lists_out = {'items': []}
lists_out['items'] = lists
json = json.dumps(lists_out)
with open('data.json', 'w') as fh:
    fh.write(json)
