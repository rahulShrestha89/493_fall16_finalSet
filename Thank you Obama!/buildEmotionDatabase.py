# Create Emotion Vector for given Image

import http.client, urllib.request, urllib.parse, urllib.error, base64, json, pickle

# Read API Key
apiFile = open('secrets.txt', 'r')
apiFile.readline();
apiKey = apiFile.readline().replace("\n", "")

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': apiKey,
}

params = urllib.parse.urlencode({
})

emotions = ["anger", "contempt", "disgust", "fear", "happiness", "neutral", "sadness", "surprise"]

def getEmotionsVector(url):
    requestBody = '{ "url" : "' + url + '" }'
    emotionsVector = [];
    try:
        conn = http.client.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/emotion/v1.0/recognize?%s" % params, requestBody, headers)
        response = conn.getresponse()
        # data = response.read()

        str_response = response.read().decode('utf-8')
        #print("**************")
        #print(str_response)
        #print("**************")
        if str_response[2:7] == "error":
            return emotionsVector;
        #print("abac")
        json_obj = json.loads(str_response)

        numFaces = len(json_obj)

        if numFaces != 1:
            return emotionsVector
        for face in json_obj:
            #print(face)
            for e in emotions:
                emo = face['scores'][e];
                emotionsVector.append(emo)
        conn.close()

    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    return emotionsVector

#url = "https://img.buzzfeed.com/buzzfeed-static/static/enhanced/terminal05/2012/5/10/10/enhanced-buzz-22789-1336660082-20.jpg";
#url = "http://www.bing.com/cr?IG=66EB97E0E19245149E9F5E6347FE4671&CID=17E031595EA36DF234B438925F926CAD&rd=1&h=MqZ63fU6T4OyNz_QEpTbfIiwuWqcXvMThVwfOXBEEYE&v=1&r=http%3a%2f%2fwww.bdlive.co.za%2fincoming%2f2016%2f01%2f05%2fbarack-obama-january-5-2016%2fALTERNATES%2fcrop_638x402%2fBarack%2bObama%2bJanuary%2b5%2b2016&p=DevEx,5038.1";
#url = "http://www.bing.com/cr?IG=66EB97E0E19245149E9F5E6347FE4671&CID=17E031595EA36DF234B438925F926CAD&rd=1&h=SIKaARWmMJTHvG8E1nhiGEXndmG1ba_KLAt28CU43Rk&v=1&r=http%3a%2f%2fi2.cdn.turner.com%2fcnnnext%2fdam%2fassets%2f160202123408-barack-obama-january-29-2016-large-169.jpg&p=DevEx,5062.1"

#vec = getEmotionsVector(url);

#print(vec)









