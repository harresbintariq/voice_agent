# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 16:03:53 2019

@author: harres.tariq
"""

from __future__ import print_function
import pyaudio
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from threading import Thread
from text_int import answer

try:
    from Queue import Queue, Full
except ImportError:
    from queue import Queue, Full

print('start')

CHUNK = 1024

BUF_MAX_SIZE = CHUNK * 10

q = Queue(maxsize=int(round(BUF_MAX_SIZE / CHUNK)))

audio_source = AudioSource(q, True, True)

close=0
# initialize speech to text service
speech_to_text = SpeechToTextV1(
    iam_apikey='XD57XU9ACmYNwBs5NVrzBuYypvpOfqehZF8p3OFRP_nP')
    #url='{YOUR_GATEWAY_URL}')


class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_transcription(self, transcript):
        #print(transcript)
        if transcript[0]['confidence']>0.4:
            print(transcript[0]['transcript'].lower())
            stream.stop_stream()
            answer(transcript[0]['transcript'].lower())
            stream.start_stream()
#            while(q.qsize()>0):
#                print(q.get())
                

    def on_connected(self):
        print('Connection was successful')

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

    def on_listening(self):
        print('Service is listening')

    def on_hypothesis(self, hypothesis):
        #print(hypothesis)
#        if(hypothesis[0]['confidence']>0.5):
#            print(hypothesis[0]['transcript'])
        pass

    def on_data(self, data):
        print(data)
        #print('me')
        pass

    def on_close(self):
        print("Connection closed")
        global close
        close=1
#        recognize_thread = Thread(target=recognize_using_weboscket, args=())
#        recognize_thread.start()
    


def recognize_using_weboscket(*args):
    mycallback = MyRecognizeCallback()
    speech_to_text.recognize_using_websocket(audio=audio_source,
                                             content_type='audio/l16; rate=44100',
                                             recognize_callback=mycallback,
                                             interim_results=True)


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100


def pyaudio_callback(in_data, frame_count, time_info, status):
    try:
        q.put(in_data)
    except Full:
        pass # discard
    return (None, pyaudio.paContinue)



while True:
    audio = pyaudio.PyAudio()
    
    
    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
        stream_callback=pyaudio_callback,
        start=False
    )
    
    
    print("Enter CTRL+C to end recording...")
    stream.start_stream()
    
    try:
        recognize_thread = Thread(target=recognize_using_weboscket, args=())
        recognize_thread.start()
    
        while True:
            if(close==1):
                print('restarting')
                close=0
                break
            pass
    except KeyboardInterrupt:
        # stop recording
        print('here')
        stream.stop_stream()
        stream.close()
        audio.terminate()
        audio_source.completed_recording()
        
        
    #print('end of loop')   
        
        
        