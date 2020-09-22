import json
import urllib.request
import numpy as np
import matplotlib.pyplot as plt
import hashlib
import datetime
import os.path
from os import path

URL = "https://data.rivm.nl/covid-19/COVID-19_casus_landelijk.json"
LOCAL = "./data"

def main():
    dateInput = input("Voor welke datum wilt u data ophalen (YYYYMMDD, leeg voor vandaag): ")

    dateChosen = 0

    if len(dateInput) != 0 and "0" <= dateInput[0] <= "9":
        if not path.exists(path.abspath(LOCAL + "/" + dateInput)):
            raise Exception("Datum niet beschikbaar")
        dateChosen = datetime.datetime.strptime(dateInput, '%Y%m%d')
    else:
        dateChosen = datetime.datetime.today()

    DataFile = getData(URL, dateChosen)
    DataJSON = json.loads(DataFile)

    cases = []
    for case in DataJSON:
        year  = int(case['Date_statistics'][0:4])
        month = int(case['Date_statistics'][5:7])
        day   = int(case['Date_statistics'][8:10])

        caseDate   = datetime.datetime(year , month, day)
        caseGender = case['Sex'][0]
        caseAge    = case['Agegroup']

        cases.append(Case(caseDate, caseGender, caseAge))


    date = datetime.datetime(2020, 1, 1)

    i = 0

    caseNumbers = []

    while date + datetime.timedelta(days=i) <= dateChosen:
        caseNumbers.append(casesOnDay(cases, date + datetime.timedelta(days=i)))
        i += 1

    dateString = (dateChosen).strftime("%Y%m%d")
    with open(path.abspath(LOCAL + "/" + dateString) + "/cases.txt", "w+") as writeFile:
        print(caseNumbers, file=writeFile)

    plt.plot(caseNumbers, label="Totaal gevallen")

    plt.ylabel("Aantal gevallen")
    plt.xlabel("Dagen sinds 1-1-2020")

    plt.legend()

    if not path.exists("plots/"):
        os.mkdir("plots/")
        
    plt.savefig("plots/" + dateString + ".png")

    plt.show()

def getStatistic(data, filterFunction):
    return [case for case in data if filterFunction(case)]

def casesOnDay(data, date):
    raw = getStatistic(data, lambda x : x.reportDate == date)
    return len(raw)

class Case:
    def __init__(self, reportDate, gender, ageGroup):
        self.reportDate = reportDate
        self.gender     = gender
        self.ageGroup   = ageGroup

    def __str__(self):
        return self.reportDate.strftime("%Y-%m-%d") + " " + self.gender

    def __repr__(self):
        return self.__str__()

def getData(url, day):
    dateString = day.strftime("%Y%m%d")

    pathLocation = path.abspath(LOCAL + "/" + dateString)
    fileName =  hashlib.md5(URL.encode('utf-8')).hexdigest() + ".json"
    totalPath = pathLocation + "/" + fileName

    if not path.exists(pathLocation):
        os.mkdir(pathLocation)

    if not path.exists(totalPath):
        fileWriter = open(totalPath, "w+")
        data = getOnlineFile(url)
        print(data, file=fileWriter)

        fileWriter.close()
        return data

    fileHandler = open(totalPath)
    data = fileHandler.read()
    fileHandler.close()

    return data

def getOnlineFile(url):
    response = urllib.request.urlopen(url)
    data = response.read()
    return data.decode('utf-8')

if __name__ == "__main__":
    main()
