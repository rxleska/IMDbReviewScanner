from nltk.corpus import wordnet

syns = wordnet.synsets('many')
for syn in syns:
    print(syn.pos())
