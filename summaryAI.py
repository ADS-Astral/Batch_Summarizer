#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 20:17:18 2020

@author: lonedingo
"""

#glob finds the files for opening
import glob
import os
 #Spacy is the abstractive summarizer library      
import spacy
#Stop words model for removing 0-value words for NLP
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
        
################Change this value to make the summary larger or smaller########        
PERCENTAGE_TO_BE_SCALED_BY = 0.05 
###############################################################################



######************MUST BE CHANGED*******************##########################
os.chdir(r'ABSOLUTE DIRECTORY PATH WHERE PAPERS ARE STORED')
##############################################################################

##############open all txt files##############################################
myFiles = glob.glob('*.txt')
print(myFiles)
for i in myFiles:
    print(i)
    
    with open(i, 'r') as file:
        text = file.read().replace('\n', '')
        text = text.lower()
        

        
###### Format the text to remove words with no significance################### 
        
        stopwords = list(STOP_WORDS)
        
        nlp = spacy.load('en')
        
        doc = nlp(text)
        
        tokens = [token.text for token in doc]
        
        #print(tokens)
        
        punctuation = punctuation + '\n'
        
        #print(punctuation)
######### Organise words by there frequency of use############################
        word_frequencies = {}
        #For words in doc that aren't part of stopwords & punctuation 
        #Score the remaining words for importance
        for word in doc:
            if word.text.lower() not in stopwords:
                if word.text.lower() not in punctuation:
                    if word.text not in word_frequencies.keys():
                        word_frequencies[word.text] = 1
                    else:
                        word_frequencies[word.text] += 1
        #print(word_frequencies)
        max_frequency = max(word_frequencies.values())
        #print(max_frequency)
        
        
########### Normalise the score###############################################
        
        for word in word_frequencies.keys():
            word_frequencies[word] = word_frequencies[word]/max_frequency
            #print(word_frequencies)
            
            sentance_tokens = [sent for sent in doc.sents]
            #print(sentance_tokens)
            
########### Proritize specific sentences###################################### 
            sentance_scores = {}
            for sent in sentance_tokens:
                for word in sent:
                    if word.text.lower() in word_frequencies.keys():
                        if sent not in sentance_scores.keys():
                            sentance_scores[sent] = word_frequencies[word.text.lower()]
                        else:
                            sentance_scores[sent] += word_frequencies[word.text.lower()]
        #print(sentance_scores)
        
        


        
        select_length = int(len(sentance_tokens)*PERCENTAGE_TO_BE_SCALED_BY)
        select_length
        
        summary = nlargest(select_length, sentance_scores, key = sentance_scores.get)
        
##########leaving a  gap between summaries in terminal#########################
        print("/n")
        print("/n")
        print("/n")
        print("/n")
        print(summary)
       
##############################################################################

#############Store summaries a indervidual text files#########################

        filename = i 
        filename_out = filename + "summarized.txt"
        text_file = open(filename_out, "w")
        n = text_file.write(str(summary).strip('[]'))
        text_file.close()
##############################################################################