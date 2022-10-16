import joblib
import os
import pandas as pd

sectorDictionary = eval(open(os.getcwd() + os.sep + "dictionaries.txt", "r").read().split("\n")[0])
countryDictionary = eval(open(os.getcwd() + os.sep + "dictionaries.txt", "r").read().split("\n")[1])
class Company:
    def __init__(self, Ticker, sector, country, marketCap, earningsGrowth, environmentScore, socialScore, governanceScore):
        self.sectorDictionary = sectorDictionary
        self.countryDictionary = countryDictionary
        self.Ticker = Ticker
        self.sector = sector
        self.country = country
        self.marketCap = marketCap
        self.earningsGrowth = earningsGrowth
        self.Emodel = joblib.load(os.getcwd() + os.sep + "EModel.joblib")
        self.Smodel = joblib.load(os.getcwd() + os.sep + "SModel.joblib")
        self.Gmodel = joblib.load(os.getcwd() + os.sep + "GModel.joblib")
        self.environmentScore = (environmentScore + self.predict(self.Emodel))/2
        self.socialScore = (socialScore + self.predict(self.Smodel))/2
        self.governanceScore = (governanceScore + self.predict(self.Gmodel))/2
    def predict(self, model):
        data = {"Sector": self.sectorDictionary[self.sector], "Country": self.countryDictionary[self.country], "MarketCap": self.marketCap, "EarningsGrowth": self.earningsGrowth}
        return float(model.predict(pd.DataFrame(data=data, index=[0])))
    def normalized(self):
        total = sum([self.environmentScore, self.socialScore, self.governanceScore])
        return [self.environmentScore/total, self.socialScore/total, self.governanceScore/total]
f = open(os.getcwd() + os.sep + "Data.txt", "r").read().split("\n")
Companies = []
for a in f[:-1]:
    adgaf = eval(a)
    Companies.append(Company(adgaf["Ticker"], adgaf["sector"], adgaf["country"], adgaf["marketCap"], adgaf["earningsGrowth"], adgaf["environmentScore"], adgaf["socialScore"], adgaf["governanceScore"]))
def companiesList():
    return Companies
def dictionaries():
    return sectorDictionary, countryDictionary