#now the same thing, but more complex
#read from a file
#run this in the termiuanl python -m spacy download en_core_web_lg to install spacy

import os

import pandas as pd
import numpy as  np
import re
import spacy
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd


from queue import Queue
import random


topicq = Queue()






def generate_poem():
    while topicq.empty() == False:
        print("generating poem")
        WORD = topicq.get()

        """this is the webscraping code so we can get poems and spilt them into to sentences"""
        #this trick the server to think that we are connecting from a web browser
        class AppURLopener(urllib.request.FancyURLopener):
            version = "Mozilla/9.0" 
        opener = AppURLopener() 

        poets = ["william-shakespeare-poems", "sylvia-plath-poems", "robert-frost-poems"]

        writer = random.choice(poets)


        data = opener.open('https://mypoeticside.com/poets/' + writer).read().decode()


        
      

        #search and save the poem links 
        soup =  BeautifulSoup(data, 'html.parser')
        poem_list = soup.find(class_="list-poems")
        links = poem_list.findAll('a')
        results = ["https:"+link.get('href') for link in links]

       
        #saves the title and content of each poem
        titles = []
        corpus = []
        for page in results:
            data = opener.open(page).read().decode()
            soup = BeautifulSoup(data, 'html.parser')
            title = soup.find(class_='title-poem')
            poem = soup.find(class_='poem-entry')
            titles.append(title.getText())
            corpus.append(poem.find('p').getText())
            
        #saves to a .csv file all the poems   
        poems = pd.DataFrame({'title' : titles,'text' : corpus})
        poems.to_csv('poems.csv')

        #function that split the poems in sentences, clean them and save them to a  *.csv
        def docs_to_sentences(file, split=r"\n"):
            path = os.getcwd()
            df_docs = pd.read_csv(path+"/" + file)
            number_docs = df_docs.shape[0]
            df_sentences = pd.DataFrame(columns=['doc_id','sentence'])  
          