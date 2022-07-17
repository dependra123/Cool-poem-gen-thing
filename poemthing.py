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
            for i in range(number_docs):
                text = df_docs.text[i]
                #dictionary to replace unwanted elements
                replace_dict = {'?«' :  '«', '(' :  '', ')' : '', ':' : ',', '.' : ',', ',,,' : ','}
                for x,y in replace_dict.items():
                    text = text.replace(x, y)
                text = text.lower()   
                #split into sentences
                sentences = re.split(split, text)
                len_sentences = len(sentences)   
                doc_id = [i] * (len_sentences)
                #save sentence and poem_id
                doc_sentences = pd.DataFrame({'doc_id' : doc_id, 'sentence' : sentences})
                df_sentences = df_sentences.append(doc_sentences)   
            #extra cleaning and reset index
            df_sentences = df_sentences[df_sentences.sentence != '']
            df_sentences.reset_index(drop=True, inplace=True)  
            #saves clean sentences to a .csv file 
            df_sentences.to_csv("sentences_" + file)
            
        #saves sentences to  sentences_poems.csv file 
        df = docs_to_sentences(file='poems.csv', split=r"\n")
        #function to generate a poem
        def poem_generator(file, word, n_sents=5):
                #load the english model from Spacy
                nlp = spacy.load("en_core_web_lg")
                init_str = nlp(word)
                path = os.getcwd()
                sentences = pd.read_csv(path+'/'+ file)
                sup_index= sentences.shape[0]
                poem_id = int()
                poem =[]
                #generate the sentences
                for i in range(n_sents):
                    rand_sent_index = np.random.randint(0, sup_index, size=30)
                    sent_list = list(sentences.sentence.iloc[rand_sent_index])
                    #transform sentences to a Spacy Doc object
                    docs = nlp.pipe(sent_list)
                    sim_list = []
                    #compute similarity for each sentence
                    for sent in docs:
                        similarity = (init_str.similarity(sent))
                        sim_list.append(similarity)
                    #saves similarity to DataFrame
                    df_1 = pd.DataFrame({'similarity' : sim_list, 'doc_id' : sentences.doc_id.iloc[rand_sent_index] }, index=rand_sent_index)   
                    df_1 = df_1[df_1.doc_id != poem_id]
                    df_1.sort_values(by='similarity', inplace=True, ascending=False)
                    sent_index= df_1.index[0]
                    sent = sentences.sentence[sent_index]
                    #erase line jumps and carriage return
                    replace_dict = {'\n' :  '', '\r' :  ''}
                    for x,y in replace_dict.items():
                        sent = sent.replace(x, y)
                    poem.append(sent)    
                    poem_id = df_1.doc_id.iloc[0]
                    init_str = nlp(sent)  
                #join the sentences with a line break
                str_poem = ("\n".join(poem)) 
                return str_poem

        #generate a poem with initial word ='fear'
        poem = poem_generator(file='sentences_poems.csv',word=WORD)
        #function to uppercase first letter and add a dot to the end
        def format_poem(text):
            text = text[:1].upper() + text[1:]
            
            text = text[:-1] + '.'
            return text   

      
        final_poem = format_poem(poem)
        print(final_poem)

        
    return True




    