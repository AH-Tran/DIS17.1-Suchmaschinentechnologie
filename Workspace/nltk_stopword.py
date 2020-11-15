from nltk.corpus import stopwords
sw = stopwords.words("english")
MyFile=open('nltk_stopwords.txt','w')
for element in sw:
     MyFile.write(element)
     MyFile.write('\n')
MyFile.close()