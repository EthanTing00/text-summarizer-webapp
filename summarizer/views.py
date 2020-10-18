from django.shortcuts import render
from django.http import HttpResponse
import nltk
import re

def homeView(request):
    return render(request, 'home.html')

def summary(request):
    stringText = request.GET['newText']
    formattedStringText = re.sub('[^a-zA-Z]', ' ', stringText)
    formattedStringText = re.sub('\s+', ' ', formattedStringText)
    #print(formattedStringText)


    sentences = nltk.sent_tokenize(stringText)
    #print(sentences)

    frequencyDictionary = {}
    stopwords = nltk.corpus.stopwords.words('english')
    #print(stopwords)

    for word in nltk.word_tokenize(formattedStringText):
        if word not in stopwords and word not in frequencyDictionary:
            frequencyDictionary.update({word:1})
        elif word not in stopwords and word in frequencyDictionary:
            frequencyDictionary[word] += 1
    #    else:
    #        frequencyDictionary[word] = 1
    #print(frequencyDictionary)

    maxFrequencyValue = max(frequencyDictionary.values())
    for word in frequencyDictionary:
        frequencyDictionary[word] = frequencyDictionary[word]/maxFrequencyValue
    #print(frequencyDictionary.keys())

    scores = {}
    for sentence in sentences:
        for word in nltk.word_tokenize(sentence.lower()):
            if word in frequencyDictionary.keys() and sentence not in scores:
                scores.update({sentence : frequencyDictionary[word]})
            elif word not in frequencyDictionary.keys():
                continue
            else:
                scores[sentence] += frequencyDictionary[word]
    #print(scores)

    sortedSentences = sorted(scores, key = scores.get, reverse=True)
    #print(sortedSentences)

    summary = ''
    for i in range(0,len(sortedSentences)//10 + 1):
        summary += sortedSentences[i]

    return render(request, 'home.html', {'result':summary})


