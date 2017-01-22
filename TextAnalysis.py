import http.client, urllib.request, urllib.parse, urllib.error, base64

#Required json format, language is optional
#{
#  "documents": [
#    {
#      "language": "string",
#      "id": "string",
#      "text": "string"
#    }
#  ]
#}
def getkeyphrases(body):
    # Request headers
    headers = {'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': 'c558677e0f9245598fc466f7eb0989b7'}
    # Request parameters
    params = urllib.parse.urlencode({'numberOfLanguagesToDetect': '{1}'})

    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/text/analytics/v2.0/keyPhrases?%s" % params, str(body), headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    return data

body = {
    "documents": [
        {
            "id": "1",
            "text": "First document. Hello world. I'm awesome."
        },
        {
            "id": "2",
            "text": "Final document. Calling Cognitive API again."
        }
    ]
    }
print(getkeyphrases(body))