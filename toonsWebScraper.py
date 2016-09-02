#!/usr/bin/env python

from bs4 import BeautifulSoup
import requests
import re
import lxml
import json

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

def pythonJsonWriter(jsonIn):
  with open('data.json', 'w') as outfile:
    json.dump(jsonIn, outfile)


wikipediaPages =["https://en.wikipedia.org/wiki/Looney_Tunes_and_Merrie_Melodies_filmography_(1929-39)",
               "https://en.wikipedia.org/wiki/Looney_Tunes_and_Merrie_Melodies_filmography_(1940-49)",
               "https://en.wikipedia.org/wiki/Looney_Tunes_and_Merrie_Melodies_filmography_(1950-59)",
               "https://en.wikipedia.org/wiki/Looney_Tunes_and_Merrie_Melodies_filmography_(1960-69)",
               "https://en.wikipedia.org/wiki/Looney_Tunes_and_Merrie_Melodies_filmography_(1970-present_and_miscellaneous)"
]

everyEpisode = []

'''
with urllib.request.urlopen(wikipediaPages[0]) as url:
  a = url.read
'''
a = requests.get(wikipediaPages[0]).text
wikiSoup = BeautifulSoup(a,"lxml")
everyEpisode.extend(parseOneWikipediaPageSoup(wikiSoup))

pythonJsonWriter(everyEpisode)


