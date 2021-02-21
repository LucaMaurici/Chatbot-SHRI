import json 
import numpy as np
from sklearn.preprocessing import LabelEncoder
from tensorflow import keras
from Laurel import Laurel
import random
import pickle
import speech_recognition as sr

class notsure(Exception):
    pass

def chat():
    # load trained model
    model = keras.models.load_model('model')

    # load tokenizer object
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    # load label encoder object
    with open('labelEncoder.pkl', 'rb') as enc:
        lbl_encoder = pickle.load(enc)

    # parameters
    max_len = 20
    
    continueConversation = True
    while continueConversation:

        guess = assistent.hear()
        inp = guess["transcription"]
        #try:
        result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]),
                                             truncating='post', maxlen=max_len))
        print(np.max(result))
        if np.max(result) < 0.5:
            raise notsure

        best_prediction = [np.argmax(result)]
        tag = lbl_encoder.inverse_transform(best_prediction)
        print(tag)
        
        method = None 
        method = getattr(assistent, tag[0])
        #print(method)
        continueConversation = method(inp)
        #except notsure:
            #assistent.speak("I'm not sure of what you have asked to me. Try with a different formulation of the sentence")
        #except:
            #assistent.speak("I didn't catch that. What did you say?")

#print("Start messaging with the bot (type quit to stop)!")

if __name__ == '__main__':
    with open("intents.json") as file:
        data = json.load(file)
    PROMPT_LIMIT = 5
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    assistent = Laurel(recognizer, microphone, PROMPT_LIMIT)
    chat()
    
    
    
    
    
    
    
    
    
    
    
    