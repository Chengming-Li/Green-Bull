import pandas as pd
from sklearn.tree import DecisionTreeRegressor
import joblib
import yfinance as yf
import time
import random
import os

# load data
data = pd.read_csv("sustainability_scores.csv")
tickers = [a for a in data["Ticker"] if a == a]

sector = []
country = []
marketCap = []
earningsGrowth = []
Eesg = []
Sesg = []
Gesg = []
def getAttr(attr, information, g=0):
    if attr in information.keys() and information[attr] != None:
        return information[attr]
    else:
        return g

for t in tickers:
    startTime = time.time()
    y = yf.Ticker(t)
    if y.info:
        yi = y.info
        sector.append(getAttr("sector", yi))
        country.append(getAttr("country", yi))
        marketCap.append(getAttr("marketCap", yi))
        earningsGrowth.append(getAttr("earningsGrowth", yi, 1))
    else:
        sector.append(0)
        country.append(0)
        marketCap.append(0)
        earningsGrowth.append(0)
    if type(y.sustainability) != type(None):
        ys = y.sustainability
        Eesg.append(ys["Value"].to_dict()["environmentScore"])
        Sesg.append(ys["Value"].to_dict()["socialScore"])
        Gesg.append(ys["Value"].to_dict()["governanceScore"])
    else:
        ind = list(data["Ticker"]).index(t)
        Eesg.append(data["Environmental SCORE"].at[ind])
        Sesg.append(data["Social SCORE"].at[ind])
        Gesg.append(data["Governance SCORE"].at[ind])
    endTime = time.time()
    elapsedTime = endTime - startTime
    print('Execution time:', elapsedTime, 'seconds')

def createDict(arr):
    ar = list(set(arr))
    return {ar[i]:i for i in range(len(ar))}
sectorDict = createDict(sector)
countryDict = createDict(country)
sector = [sectorDict[i] for i in sector]
country = [countryDict[i] for i in country]
f = open(os.getcwd() + os.sep + "dictionaries.txt", 'w')
f.write(str(sectorDict))
f.write("\n" + str(countryDict))
CompleteData = pd.DataFrame(data={"Ticker":tickers, "Sector": sector, "Country": country, "MarketCap": marketCap, "EarningsGrowth":earningsGrowth, "E": Eesg, "S": Sesg, "G": Gesg})
X = CompleteData[["Sector", "Country", "MarketCap", "EarningsGrowth"]]
eData = CompleteData["E"]
sData = CompleteData["S"]
gData = CompleteData["G"]

def saveModel(data, name):
    global X_test
    global Y_Test
    model = DecisionTreeRegressor()
    model.fit(X, data)
    joblib.dump(model, f"{name}.joblib")
saveModel(eData, "EModel")
saveModel(sData, "SModel")
saveModel(gData, "GModel")