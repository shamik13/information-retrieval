import os, fnmatch, re, sets, heapq, nltk, requests, numpy, matplotlib.pyplot as plt
from collections import defaultdict
from bs4 import BeautifulSoup
from math import log10
from nltk.stem import PorterStemmer
from nltk.stem.snowball import SnowballStemmer

dct = defaultdict(list)

docDirectory = "crawlDir/"
stopWordList = []
totalDocs = 1000
K = 20
DEBUG = 0

def createStopWord():
    global stopWordList
    url="http://www.lextek.com/manuals/onix/stopwords1.html"
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text,"html.parser")
    list = []
    for word in soup.findAll('blockquote'):
        list.append(word)
    word2=str(list[0]).split()
    stopWordList = word2[77:503]
    print "*******************" + str(stopWordList) + "********************"

def isStopWord(term):
    term1=term.lower()
    if term1 in stopWordList or len(term1)<=2:
        return True
    else:
        return False

def calculateAvgGap(lst):
    if DEBUG:
        print lst
    for i in range(K-1):
        sum = 0
        word = lst[i][1]
        postingLst = dct[word]
        postingLst = list(set(postingLst)) #To retrieve unique docIds
        for j in range(0, len(postingLst)-1):
            sum = sum + abs(postingLst[j] - postingLst[j+1])
        print str(word) + ": " + str((float)(sum)/(float)(len(postingLst)-1))

def statisticalAnalysis():
    arr = []
    for key, value in dct.items():
        arr.append((len(set(value)), key))

    # Sorting the list based on the its document-frequency
    arr.sort()
    print str(arr)
    elemCnt = len(arr)

    # Least Frequent
    freq = []
    for item in range(K):
        freq.append(arr[item])
    print "\nLeast Frequent Words:\n" + str(freq)
    calculateAvgGap(freq)

    # Most Frequent
    freq = []
    for item in range(elemCnt-1, elemCnt-1-K, -1):
        freq.append(arr[item])
    print "\nMost Frequent Words:\n" + str(freq)
    calculateAvgGap(freq)

    # Median Frequent
    freq = []
    for item in range(elemCnt/2 - K/2, elemCnt/2 + K/2):
        freq.append(arr[item])
    print "\nMedian Frequent Words:\n" + str(freq)
    calculateAvgGap(freq)

def stemming(term):
    #stemmer=PorterStemmer()
    #stemmed=stemmer.stem(term)
    stemmed1= SnowballStemmer("english").stem(term)
    return str(stemmed1)

def calculateIndexChar(indexName, dictionary ):
    dctLen = len(dictionary)
    max = 0
    min = 9999999
    totalLen = 0
    elems = 0
    for word, list in dictionary.items():
        elems = elems + 1
        listLen = len(list)
        if max < listLen:
            max = listLen
        if min > listLen:
            min = listLen
        totalLen = totalLen + listLen
    print "\nCharacteristics of Index " + str(indexName) + ":"
    print "Number of Terms: " + str(dctLen)
    print "Maximum length of Postings List: " + str(max)
    print "Minimum length of Postings List: " + str(min)
    print "Average length of Postings List: " + str(totalLen/dctLen)
    print "Size of file: " + str((float)(os.path.getsize(indexName + ".txt"))/(float)(1024)) + " KB\n"

def makeInvertedIndex(indexName, dictonary):
    with open(indexName + ".txt", "w") as file:
        for item in dictonary.items():
            file.write(str(item)+"\n")
    file.close()
    calculateIndexChar(indexName, dictonary)

def makeI1(dctOld):
    #Original Index
    makeInvertedIndex("I1",dctOld)

def makeI2(dctOld):
    # Stop Word Removal
    dctNew = defaultdict(list)
    for word in dctOld:
        if not isStopWord(word):
            if DEBUG:
                print("Deleted Word: " + word)
            dctNew[word]=dctOld[word]
    makeInvertedIndex("I2",dctNew)
    return dctNew

def makeI3(dctOld):
    # Stemming
    dctNew = defaultdict(list)
    for word in dctOld:
        try:
            stemmedWord = stemming(word)
        except:
            print "----- To Do Handle: " + word + " -----"
            continue

        if word != stemmedWord:
            if DEBUG:
                print(word + " | " + stemmedWord)
            for docIds in dctOld[word]:
                dctNew[stemmedWord].append(docIds)
            if DEBUG:
                print(dctOld[word])
                print(dctNew[stemmedWord])
        else:
            dctNew[word] = dctOld[word]
    makeInvertedIndex("I3", dctNew)
    return dctNew

def makeI4(dctOld):
    # Do not consider terms which are occurring in < 2% of  the documents
    dctNew = defaultdict(list)
    for word,item in dctOld.items():
        # To remove repititions
        item = list(set(item))
        if len(item) >= (0.02 * totalDocs):
            dctNew[word]=dctOld[word]

    makeInvertedIndex("I4", dctNew)
    return dctNew

def createGraph(graphList, xLabel, yLabel, plotName):
    xAxis = []
    yAxis = []
    for item in graphList:
        xAxis.append(item[0])
        yAxis.append(item[1])

    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.scatter(xAxis,yAxis)
    plt.plot(xAxis,yAxis)
    try: # Remove file, if already exists
        os.remove(plotName + ".png")
    except:
        pass
    plt.savefig(plotName + ".png")
    plt.close()

# Procedure Init
if __name__ == "__main__":
    date=[]
    t=''
    for i in [1,31]:
        date.append(str(i))
    for docNum in range(1, totalDocs+1):
        with open(docDirectory + str(docNum) + ".txt") as file:
            for line in file:
                #Considering only lowercase characters
                line = str(line.lower())
                date = re.findall(r'(\s)+((\d*){1,4}(\s*)(?:january|february|march|april|may|june|july|august|september|october|november|december)(\s+)(\d+){1,4}(x*\d*){1,4})\s', line)
                if date:
                  #  print "Date Found: |" + str(date[0][1]) + "|"
                    mod = date[0][1].replace(' ','')
                    line = re.sub(date[0][1], mod, line)
                   # print "Date Modified: " + str(line)

                for word in re.split(' ', line):
                    #for removing fullstops, commas and other not useful data
                    if not fnmatch.fnmatch(word, "*:"):
                        if fnmatch.fnmatch(word, "http*") or fnmatch.fnmatch(word, "*-*-*"):
                            pass
                        else:
                            word = re.sub(r'[^\w]', '', word)
                        if word != '' and word != 'doc':
                            word = re.sub(r'\n', '', word)
                            dct[word].append(docNum)

    #Stop Word Filtering and Stemming
    createStopWord()
    makeI1(dct)       # Original Index
    dct = makeI2(dct) # Stop Word removal
    dct = makeI3(dct) # Stemming
    dct = makeI4(dct) # Remove less frequent words

    # Statistical Analysis
    statisticalAnalysis()

    #Create Log Graph - I
    topcollect = []
    topfreq = []
    termsfreq=[(word,len(items)) for word,items in dct.items()]
    termsfreq=sorted(termsfreq, key=lambda x: x[1], reverse=True)
    topcollect=[word for (word,freq) in termsfreq if len(topcollect)<1000]
    topfreq=[freq for (word,freq) in termsfreq if len(topfreq)<1000]

    graphList = []
    for i in range(1, len(topfreq)):
        graphList.append((log10(i), log10(topfreq[i])))

    createGraph(graphList, "log(Rank of the Term)", "log(Collection Frequency of the Term)", "logRankCollectionFreq")

    #Create Log Graph - II
    graphList = []
    vocabularyObs = []
    tokenCount = 0
    for docId in range(1, totalDocs+1):
        for key,list in dct.items():
            occurences = list.count(docId)
            tokenCount = tokenCount + occurences
            if occurences and key not in vocabularyObs:
                vocabularyObs.append(key) #Add to vacabulory
        graphList.append((log10(tokenCount), log10(len(vocabularyObs))))

    createGraph(graphList, "log(#Tokens observed)", "log(#Vocabulory observed)", "logTokenVacabulary")
