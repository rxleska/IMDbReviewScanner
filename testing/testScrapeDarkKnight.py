import requests
from bs4 import BeautifulSoup as bs
import json
from io import BytesIO
import re
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords

#Create union words array (common words that we don't want)
with open("unionWords.txt", "r") as unionWords:
    uWords = unionWords.read().replace('\n', '')
s = uWords.split(',')

# load more data key http://www.imdb.com/{data-ajaxurl}?paginationKey={data-key}
# original url "https://www.imdb.com/title/tt0468569/reviews?ref_=tt_ql_3"

#gets all the html from the dark knight reviews page
url = 'https://www.imdb.com/title/tt0468569/reviews?ref_=tt_ql_3'
html = requests.get(url).text



#need to get all reviews data-ajaxurl contains next ajax code
curhtml = html
start = 'data-key=\"'
end = "\""
curUrlKey = ''
curUrl = ''
count = 0
while "data-key" in curhtml:
        if count >= 79:
            print("Done!")
            break
        count+=1
        curUrlKey = curhtml.split(start)[1].split(end)[0]
        curUrl = "http://www.imdb.com/title/tt0468569/reviews/_ajax?paginationKey="+ curUrlKey
        curhtml = requests.get(curUrl).text
        html = html + "\n<b>SEPARATOR\n</b>" + curhtml
        #print(curhtml)
# with open('divSort.json', 'w', encoding="utf-8") as outfile:
#     outfile.write(html.__str__())


#create soup
soup = bs(html,'html.parser')



#get all div tags
allDivs = []
allDivs = soup.findAll('div')

#number of divs without a class defined
numWOClass = 0

#find all class="text show-more__control" divs # two classes seen 'text', 'show-more__control' 
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
        numWOClass = numWOClass + 1
print(numWOClass)

print(len(reviews))


#get text from found divs 
words = []
for revs in reviews:
    words = words + revs.split(" ")

#process and make map of words
weightWords = {}
for word in words:
    word = word.lower()
    syns = wn.synsets(word)
    
    posOfWord = []
    if len(syns) != 0:
        posOfWord.append(syns[0].pos())
    #for syn in syns:
    #    posOfWord.append(syn.pos()) 
    if 'a' in posOfWord and word not in s:
        try:
            weightWords.get(word)
            weightWords[word] = weightWords.get(word) + 1
        except:
            weightWords[word] = 1
sortedWords = sorted(weightWords.items(), key=lambda x: x[1])

#remove nonadjitives 
#for

#display

with open('darkKnight.json', 'w', encoding="utf-8") as outfile:
    outfile.write(sortedWords.__str__())