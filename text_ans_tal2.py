# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#import nltk
#import sklearn
import re
#from nltk.corpus import stopwords 
import numpy as np   
from sklearn.metrics.pairwise import cosine_similarity
#from __future__ import print_function
#import json
#from os.path import join, dirname
from ibm_watson import TextToSpeechV1
from ibm_watson.websocket import SynthesizeCallback
import pyaudio

class Play(object):
    """
    Wrapper to play the audio in a blocking mode
    """
    def __init__(self):
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 22050
        self.chunk = 1024
        self.pyaudio = None
        self.stream = None

    def start_streaming(self):
        self.pyaudio = pyaudio.PyAudio()
        self.stream = self._open_stream()
        self._start_stream()

    def _open_stream(self):
        stream = self.pyaudio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            output=True,
            frames_per_buffer=self.chunk,
            start=False
        )
        return stream

    def _start_stream(self):
        self.stream.start_stream()

    def write_stream(self, audio_stream):
        self.stream.write(audio_stream)

    def complete_playing(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pyaudio.terminate()

class MySynthesizeCallback(SynthesizeCallback):
    def __init__(self):
        SynthesizeCallback.__init__(self)
        self.play = Play()

    def on_connected(self):
        print('Opening stream to play')
        self.play.start_streaming()

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_timing_information(self, timing_information):
        print(timing_information)

    def on_audio_stream(self, audio_stream):
        self.play.write_stream(audio_stream)

    def on_close(self):
        print('Completed synthesizing')
        self.play.complete_playing()


service = TextToSpeechV1(
        ## url is optional, and defaults to the URL below. Use the correct URL for your region.
        #url='https://stream.watsonplatform.net/text-to-speech/api',
        iam_apikey='49znmJ6MB8-7fuI3otG3EH-eHHaZu6PFIEwff2pQ5wBJ')
    
test_callback = MySynthesizeCallback()


stop_words = ['a',  'about', 'across', 'after',  'almost', 'also', 'am', 'among', 'an',\
              'and', 'any',
              'are', 'as', 'at', 'be', 'because', 'been', 'but', 'by', 'can', 'cannot', 'dear', 'did',
              'do', 'does', 'either', 'else', 'ever', 'every', 'for', 'from', 'get', 'got', 'had', 'has', 'have',
              'he', 'her', 'hers', 'him', 'his', 'however', 'i', 'if', 'in', 'into', 'is', 'it', 'its',
              'just', 'least', 'let', 'like', 'likely', 'may', 'me', 'might', 'most', 'must', 'my', 'neither',
              'no', 'nor', 'not', 'of', 'off', 'often', 'on', 'only', 'or', 'other', 'our', 'own', 'rather',
              'said', 'say', 'says', 'she', 'should', 'since', 'so', 'some', 'than', 'that', 'the', 'their',
              'them', 'then', 'these', 'they', 'this', 'tis', 'to', 'too', 'twas', 'us', 'wants','we'
              'was',  'were',  'while', 'whom', 'why', 'will',
              'with', 'would', 'yet',  'your']

              
questions_list = ["hello Nadia ",
                  "how are you ",
                  "What about you",
                  "Tell us about yourself ",
                  "share the recharge number for today " ,
                  "four g. forecast for october ",
                  "for g. forecast for october ",
                  "are you there ",
                  "good bye ",
                  "hi",
                  "Will we meet our target for this month?",
                  "can we acheive net adds target for this month",
                  "What is art of possibility for acheiving the target",
                  "If we want to achieve our target, what is the art of possibility?",
                  "will winter affect our closing ",
                  "will windows affect our closing ",
                  "what will be the affect of winter on our closing "
                  'does it look like we acheive the target for this month',
                  'are we going to acheive the target for this month',
                  'will we be able to acheive target for this month'
]


answers_list = [' Hello! How can I help you?',
                ' I am fine, Thank you.',
                ' I am fine, Thank you.',
                ' Sure. I am Nadia, an aspiring AI board member in training. I can answer your queries',
                ' Recharge for today is 215.3 Million as of 4pm today',
                ' Forecast for October is six hundred thousand net adds',
                ' Forecast for October is six hundred thousand net adds',
                ' I am always here. How can I help you',
                ' bye',
                ' hello',
                ' Based on a straight-line trajectory, we will be short by 5%',
                ' Based on a straight-line trajectory, we will be short by 5%',
                ' We would have to do a lot of net adds per day in order to meet our target which requires increased efforts on gross adds and conversions from 3G to 4G',
                ' We would have to do a lot of net adds per day in order to meet our target which requires increased efforts on gross adds and conversions from 3G to 4G',
                ' Based on the weather data that I have access to, we will see a 3% drop in our revenue in the coming months. However, I think your commercial team is more than capable of achieving their targets.',
                ' Based on the weather data that I have access to, we will see a 3% drop in our revenue in the coming months. However, I think your commercial team is more than capable of achieving their targets.',
                ' Based on the weather data that I have access to, we will see a 3% drop in our revenue in the coming months. However, I think your commercial team is more than capable of achieving their targets.',
                ' Based on a straight-line trajectory, we will be short by 5%',
                ' Based on a straight-line trajectory, we will be short by 5%',
                ' Based on a straight-line trajectory, we will be short by 5%'
                ]    

def clean_data(questions_list,stop_words):
    for index,question in enumerate(questions_list):
        question = re.sub('[^A-Za-z]', ' ', question)
        question = question.lower()
        for tag in stop_words:
            question = re.sub(r'\b' + tag + r'\b', '', question)
        questions_list[index] = question
    return questions_list
'''    
def make_dict(words):
    dict_syn={}
    for word in words:
        synonyms = [] 

        for syn in wordnet.synsets(word): 
            for l in syn.lemmas(): 

                synonyms.append(l.name()) 

        dict_syn[word]=list(synonyms)
    return dict_syn
'''
#calculate vector for input
def word_count(inp):
    counts = dict()
    words = inp.split()
    #complete_word_dict = make_dict(words)
    #for key,complete_word in complete_word_dict.items():
    #    words.extend(complete_word)
    #print(words)
    #print('////////////////////')
    for word in words:
        
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts

    
# Find vector for each item in the vocab
def occurence_finding(questions_list):
    
    occurence_dict = {}
    for index,question in enumerate(questions_list):
        occurence_dict[index] = word_count(question)
    return occurence_dict
    
# Find question vector for each item in the vocab
def vectorization_input_question(input_question,occurence_dict_final):
    input_question_feature_dict = {}
    for index,vocab_question in enumerate(occurence_dict_final):
        counts = dict()
        input_words = input_question.split()
        vocab_question_keys = occurence_dict_final[index].keys()#.split()
        for vocab_question_word in vocab_question_keys:
           counts[vocab_question_word] = input_words.count(vocab_question_word)
        input_question_feature_dict[index] = counts
    return input_question_feature_dict

# Extract values from vocab & question dict
def extract_value_from_dict(occurence_dict_final):
    
    norm_occurence_dict_final = []
    for index,new_dict_vocab in enumerate(occurence_dict_final):
        new_list_values = list(occurence_dict_final[index].values())
        norm_occurence_dict_final.append(new_list_values)
    return norm_occurence_dict_final 
            

#Calculate Final similarity b/w input & vocab    
def calculate_final_similarity_list(norm_input_question,norm_occurence_dict_final):
    
    final_similarity_list = []
    for index,norm_input_question_single in enumerate(norm_input_question):
        cos_lib = cosine_similarity(
                                np.array(norm_input_question[index]).reshape(1,len(norm_input_question[index])),np.array(norm_occurence_dict_final[index]).reshape(1,len(norm_occurence_dict_final[index])))
        #print(cos_lib[0][0])
        final_similarity_list.append(cos_lib[0][0])
    return final_similarity_list
            

def before_first_Sentence(questions_list,stop_words):
    questions_list = clean_data(questions_list,stop_words)    
    occurence_dict_final = occurence_finding(questions_list)
    norm_occurence_dict_final = extract_value_from_dict(occurence_dict_final)
    return questions_list,occurence_dict_final,norm_occurence_dict_final

def after_first_sentence(input_question,occurence_dict_final,norm_occurence_dict_final):
    #input_question = "What is recharge number for today"
    input_question = re.sub('[^A-Za-z]', ' ', input_question)
    input_question = input_question.lower()    
    input_question_feature_dict = vectorization_input_question(input_question,occurence_dict_final)
    norm_input_question = extract_value_from_dict(input_question_feature_dict)
    final_similarity_list = calculate_final_similarity_list(norm_input_question,norm_occurence_dict_final)
    return final_similarity_list  

def get_input(inp):
     questions_lists,occurence_dict_final,norm_occurence_dict_final = before_first_Sentence(questions_list,stop_words)
     input_question = inp
     final_similarity_list =  after_first_sentence(input_question,occurence_dict_final,norm_occurence_dict_final)
     max_index = final_similarity_list.index(max(final_similarity_list))
     if final_similarity_list[max_index] > 0.6:
         return answers_list[max_index]
     else:
         return 'Could you rephrase that please'
         
     
def answer(ques):
    ans=get_input(ques)
    try:
        SSML_text = """<speak version=\"1.0\">
            <emphasis>""" + ans +"""</emphasis>
            </speak>"""
    except:
            SSML_text = """<speak version=\"1.0\">
            <emphasis>""" + "Could you rephrase that please!" +"""</emphasis>
            </speak>"""    
    print(SSML_text)
#    service.synthesize_using_websocket(SSML_text,
#                                       test_callback,
#                                       accept='audio/wav',
#                                       voice="en-US_AllisonVoice"
#                                      )
