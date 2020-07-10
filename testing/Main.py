#used to scrape imdb
import requests
from bs4 import BeautifulSoup as bs
import json
from io import BytesIO
import re
#Used for processing the words in the reviews to remove non-adjectives 
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
#used for making the word cloud
import numpy as np 
import pandas as pd 
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
##################################################################################

#generate union word list 
with open("unionWords.txt", "r") as unionWords:
    uWords = unionWords.read().replace('\n', '')
s = uWords.split(',')


# base for search on imdb https://www.imdb.com/find?q=the+dark+knight&ref_=nv_sr_sm
# result_text is the td class 
searchName = input('Type title of movie: ')
searchName = searchName.replace(" ", "+")
searchUrl = 'https://www.imdb.com/find?q=' + searchName + '&ref_=nv_sr_sm'
print("Search Url: " + searchUrl)
searchHtml = requests.get(searchUrl).text
searchSoup = bs(searchHtml, 'html.parser')
searchTds = searchSoup.findAll('td')
#print(len(searchTds))
for td in searchTds:
    if 'result_text' in td["class"]:
        tdA = td.find('a')
        #print('td contents: ' + tdA['href'])
        break
imdbUrl = 'https://www.imdb.com' + tdA['href']


#Navagate to the first review page 
revHtml = requests.get(imdbUrl).text
revSoup = bs(revHtml, "html.parser")
revDivs = revSoup.findAll('div')
for div in revDivs:
    try:
        if div["id"] == 'quicklinksMainSection':
            aLinks = div.findAll('a')
            for a in aLinks:
                if 'USER REVIEWS' in a:
                    imdbUrl = 'https://www.imdb.com' + a['href']
                    break
    except:
        d=0
        #didnt have a div id


#get first page of reviews 
#imdbUrl = 'https://www.imdb.com/title/tt0468569/reviews?ref_=tt_ql_3'
print(imdbUrl)
html = requests.get(imdbUrl).text


#get subsequent imdb review pages
curhtml = html
curUrlKey = ''
curAjaxUrl = curhtml.split('data-ajaxurl=\"')[1].split('\"')[0]
curUrl = ''
count = 0
while "data-key" in curhtml:
        if count >= 239: # 1000 reviews 
            print("Done scraping!")
            break
        count+=1
        curUrlKey = curhtml.split('data-key=\"')[1].split("\"")[0]
        curUrl = "http://www.imdb.com"+curAjaxUrl +"?paginationKey="+ curUrlKey
        curhtml = requests.get(curUrl).text
        html = html + "\n<b>SEPARATOR\n</b>" + curhtml


#create soup
soup = bs(html, 'html.parser')


#get all div tags
allDivs = []
allDivs = soup.findAll('div')


#find all class="text show-more__control" divs 
#two classes seen 'text', 'show-more__control'
#These are the classes that the reviews are held in 
reviews = []
for div in allDivs:
    try:
        #print(div["class"])
        if('text' in div["class"]):
            rev = div.__str__()
            rev = re.sub(r'<.+?>', '', rev)
            rev = re.sub('[^a-zA-Z\d\s]', '',rev)
            reviews.append(rev)
    except:
        divclassmissing=0
print('Found ' + len(reviews).__str__() + " reviews.")


#get text from found divs
words = []
for revs in reviews:
    words = words + revs.split(' ')


#process and make dictionary of words 
weightWords = {}
for word in words:
    word = word.lower() # words to lowercase
    syns = wn.synsets(word) # get list of words 
    posOfWord = [] # list of part of speech of the word
    if len(syns) != 0:
        posOfWord.append(syns[0].pos()) # add parts of speech to arraylist
    if ('a' in posOfWord) and (word not in s): # sort words, make weight dictionary
        try:
            weightWords.get(word)
            weightWords[word] = weightWords.get(word) + 1
        except:
            weightWords[word] = 1


#sort dictonary by converting to arraylist then back to dictionary 
sortedWords = sorted(weightWords.items(), key=lambda  x: x[1], reverse=True)
wordData = dict()
for word in sortedWords:
    wordData[word[0]] = word[1]


#form word cloud weighted based on the values in the dictionary
wordcloud = WordCloud(font_path=None, width=1920, height=1080,stopwords=STOPWORDS, max_words=200).generate_from_frequencies(wordData)


#plot words 
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.savefig(searchName+".jpg" )
plt.show()
