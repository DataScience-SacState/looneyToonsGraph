#!/usr/bin/env python

import requests
import re
import lxml
import json
from bs4 import BeautifulSoup

#Globally defined data structures/variables
wikipediaPages =["https://en.wikipedia.org/wiki/Looney_Tunes_and_Merrie_Melodies_filmography_(1929-39)",
               "https://en.wikipedia.org/wiki/Looney_Tunes_and_Merrie_Melodies_filmography_(1940-49)",
               "https://en.wikipedia.org/wiki/Looney_Tunes_and_Merrie_Melodies_filmography_(1950-59)",
               "https://en.wikipedia.org/wiki/Looney_Tunes_and_Merrie_Melodies_filmography_(1960-69)",
               "https://en.wikipedia.org/wiki/Looney_Tunes_and_Merrie_Melodies_filmography_(1970-present_and_miscellaneous)"
]


def parseOneEpisodeSoup(episodeSoup):
  episode = {}
  episode["Title"] = episodeSoup[0].get_text()
  episode["Series"] = episodeSoup[1].get_text()
  myList = str(episodeSoup[2]).split("<br/>")
  animators = []
  for a in myList:
      animators.append(re.sub('<[^<]+?>', '',a).replace(",","").replace("\n",""))
  episode["Animator"] = animators

  myList = str(episodeSoup[3]).split("<br/>")
  characters = []
  for a in myList:
      characters.append(re.sub('<[^<]+?>', '',a).replace(",","").replace("\n",""))
  episode["Character"] = characters
  episode["ID"] = episodeSoup[4].get_text()
  episode["Date"] = episodeSoup[5].get_text()
  return(episode)

def parseOneYearSoup(yearSoup):
  allEpisodesList = yearSoup.find_all("tr")[1:]
  yearList = []
  for episodeSoup in allEpisodesList:
      yearList.append(parseOneEpisodeSoup(episodeSoup.find_all("td")))
  return(yearList)

def parseOneWikipediaPageSoup(wikipediaSoup):
  allYearsList = wikipediaSoup.find_all("table", class_="wikitable sortable")
  pageList = []
  for yearSoup in allYearsList:
      pageList.extend(parseOneYearSoup(yearSoup))
  return(pageList)

def pythonJsonWriter(jsonIn,count):
  with open('data' + str(count) + '.json', 'w') as outfile:
    json.dump(jsonIn, outfile)

def loopLoony(listIn):
  everyEpisode = []
  count = 0
  for links in listIn:
    a = requests.get(links).text
    wikiSoup = BeautifulSoup(a,"lxml")
    parsedTable = parseOneWikipediaPageSoup(wikiSoup)
    pythonJsonWriter(parsedTable,count)
    count+=1

def main():
  loopLoony(wikipediaPages) 

if __name__ == "__main__":
  main()
