                                                            #HOTEL RECOMMENDATION SYSTEM
import json
import requests
import pickle
import streamlit as st
from streamlit_lottie import st_lottie
import pandas as pd                                                 #Import ML Libraries
import nltk
nltk.download('wordnet')
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from ast import literal_eval



#To Customize Page Icon
from PIL import Image
img=Image.open('goibibo3.gif')
st.set_page_config(page_title='Goibibo',page_icon=img)

#To customize the Background Image
page_bg_img = '''
    <style>
    [data-testid="stAppViewContainer"]
    {
    background-image: url("https://www.1hotels.com/sites/default/files/styles/mega_menu_image_retina/public/2021-03/1_hotel01.jpg?h=a49d782d&itok=jEfYexKd");
    background-size: cover;
    
    }
    [data-testid="stHeader"]{
    background-color:rgba(0,0,0,0);
    }
    </style>
    '''
st.markdown(page_bg_img, unsafe_allow_html=True)


import requests
#Recommender System
def recommend(selected_country,description):
    description = description.lower()
    word_tokenize(description)
    stop_words = stopwords.words('english')
    lemm = WordNetLemmatizer()
    filtered = {word for word in description if not word in stop_words}
    filtered_set = set()
    for fs in filtered:
        filtered_set.add(lemm.lemmatize(fs))

    country = Hotel[Hotel['Location'] == selected_country.lower()]
    country = country.set_index(np.arange(country.shape[0]))
    list1 = []
    list2 = []
    cos = []
    for i in range(country.shape[0]):
        temp_token = word_tokenize(country["Tags"][i])
        temp_set = [word for word in temp_token if not word in stop_words]
        temp2_set = set()
        for s in temp_set:
            temp2_set.add(lemm.lemmatize(s))
        vector = temp2_set.intersection(filtered_set)
        cos.append(len(vector))
    country['similarity'] = cos
    country = country.sort_values(by='similarity', ascending=False)
    country.drop_duplicates(subset='property_name', keep='first', inplace=True)
    country.sort_values('site_review_rating', ascending=False, inplace=True)
    country.reset_index(inplace=True)
    recommends=[]
    recommends.append(country[["property_name", "site_review_rating", "address"]].head())
    return recommends

#To Add a Text Box and Select Box to the App and display the Cities List
st.header('HOTEL RECOMMENDATION SYSTEM')
Hotel= pickle.load(open('Hotel_list.pkl', 'rb'))
Similarity= pickle.load(open('similarity.pkl', 'rb'))

Hotel_list = Hotel['Location'].unique()

selected_country = st.selectbox( "Type or select a City from the dropdown",Hotel_list)
description = st.text_input('Description')

if st.button('Recommend'):
    recommendations=recommend(selected_country,description)
    for i in recommendations:
        st.write(i)
