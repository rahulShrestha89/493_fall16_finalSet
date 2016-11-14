#Build Mood Vector for each

import pickle, time

from buildEmotionDatabase import getEmotionsVector

UrlDict = pickle.load(open("faceUrls.pkl", "rb"))
#testUrlDict = {"01/2016" : UrlDict["01/2016"],
               #"02/2016" : UrlDict["02/2016"],
               #"03/2016" : UrlDict["03/2016"]}


moodDict = {}
count = 0;
for month in UrlDict.keys():
    print(month)
    moodArray = [0,0,0,0,0,0,0,0]
    numUrls = len(UrlDict[month])
    #print(numUrls)
    for url in UrlDict[month]:
        count += 1
        if count % 19 == 0:
            print("PAUSE!!!!!!!!!!!!")   # Pause (20 calls/min max)
            time.sleep(60)
        urlEmos = getEmotionsVector(url)
        #print(urlEmos)
        if len(urlEmos) == 8:
            for i in range(0,8):
                moodArray[i] += urlEmos[i]
        else:
            numUrls -= 1
    if numUrls != 0:
        for i in range(0,8):
            moodArray[i] /= numUrls
    moodDict[month] = moodArray

print(moodDict)
pickle.dump(moodDict, open("monthMoods.pkl", "wb"))
