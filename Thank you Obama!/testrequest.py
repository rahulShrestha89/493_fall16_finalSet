########### Python 3.5 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64, json, pickle

apiFile = open('secrets.txt', 'r')

apiKey = apiFile.readline().replace("\n", "")

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': apiKey,
}

# 12 Months of the year
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

# Final month (last month has no data)
finalMonth = months[11]

# First year to get data from
currentYear = 2009 

# Last month to get data from (inclusive)
finalYear = 2016

# Person to be looked up
personQuery = 'Obama'

# Index of the first month to query
monthIndex = 0 # January

# Json Object to be built up from queries
results = {}

# Function for getting the mm/yyyy representation of the current year/month 
def getMMYYYY(monthIndex, year):
    mm = monthIndex + 1
    monthString = ''
    if mm < 10:
        monthString = '0' + str(mm)
    else:
        monthString = str(mm)

    return monthString + "/" + str(year) 


# Iterates over the time range and adds urls for each month
while (currentYear <= finalYear):
    if currentYear == finalYear and months[monthIndex] == finalMonth:
        break

    # Search string to be built out of the person + month + year
    queryString = personQuery + " " + months[monthIndex] + " " + str(currentYear)  
    
    params = urllib.parse.urlencode({
        # Request parameters
        'q': queryString,
        'count': '10',
        'offset': '0',
        'mkt': 'en-us',
        'safeSearch': 'Moderate',
    })

    try:
        conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')
        conn.request("GET", "/bing/v5.0/images/search?%s" % params, "{body}", headers)
        response = conn.getresponse()

        # Add the url to the url list for the month
        str_response = response.read().decode('utf-8')
        json_obj = json.loads(str_response)
        urlList = []
        for i in range(0,10):
            contenturl = json_obj['value'][i]['contentUrl']
            urlList.append(contenturl)

        # Adds the list to the results dictionary
        monthYearKey = getMMYYYY(monthIndex, currentYear)
        results[monthYearKey] = urlList

        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    monthIndex += 1
    if monthIndex > 11:
        monthIndex = 0
        currentYear += 1

pickle.dump(results, open("faceUrls.pkl", "wb"))

print(json.dumps(results))

####################################

