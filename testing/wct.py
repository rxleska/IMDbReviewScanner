import requests
from bs4 import BeautifulSoup as bs
import json
from io import BytesIO
import re
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
import numpy as np 
import pandas as pd 
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

text = 'dude hello hi bye goodbye howdy sup'

wordcloud = WordCloud().generate(text)

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()