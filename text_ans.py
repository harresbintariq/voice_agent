# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 14:24:06 2019

@author: harres.tariq
"""
from __future__ import print_function
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
dialogue={
        'hello nadia ':' Hello! How can I help you?',
        'how are you ': ' I am fine, Thank you.',
        'tell us about yourself ':' Sure. I am Nadia, an aspiring AI board member in training. I can answer your queries',
        'share the recharge number for today ':'Recharge for today is 215.3 Million as of 4pm today',
        'what is the four g. forecast for october ':'Forecast for October is six hundred thousand net adds',
        'are you there ':' I am always here. How can I help you',
        'good bye ':'bye'
    }

def answer(question):
    # An example SSML text
    try:
        SSML_text = """<speak version=\"1.0\">
            <emphasis>""" + dialogue[question] +"""</emphasis>
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