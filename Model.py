import json 
import numpy as np 
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import callbacks
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, Flatten, GlobalAveragePooling1D, GlobalMaxPooling1D, MaxPooling1D, Dropout, Conv1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
import pickle

vocab_size = 500
embedding_dim = 16
max_len = 20
oov_token = "<OOV>"

def loaddata():
    with open('intents.json') as file:
        data = json.load(file)
        
    with open('val_intents.json') as file:
        val = json.load(file)
        
    training_sentences = []
    training_labels = []
    labels = []

    val_sentences = []
    val_labels = []


    for intent in data['intents']:
        for pattern in intent['patterns']:
            training_sentences.append(pattern)
            training_labels.append(intent['tag'])
        
        if intent['tag'] not in labels:
            labels.append(intent['tag'])

    for intent in val['val_intents']:
        for pattern in intent['patterns']:
            val_sentences.append(pattern)
            val_labels.append(intent['tag'])
            
            
    num_classes = len(labels)
    
    return training_sentences, training_labels, labels, val_sentences, val_labels, num_classes

def loadmodel():
    # load trained model
    model = keras.models.load_model('model')

    # load tokenizer object
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    # load label encoder object
    with open('labelEncoder.pkl', 'rb') as enc:
        lbl_encoder = pickle.load(enc)
        
    return model, tokenizer, lbl_encoder


def createmodel(training_labels, training_sentences):

    #encoding labels in numbers between 0 and num_classes - 1
    lbl_encoder = LabelEncoder()
    lbl_encoder.fit(training_labels)
    
    #text tokenization
    tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_token)
    tokenizer.fit_on_texts(training_sentences)
    
    #creating the model
    model = Sequential()
    model.add(Embedding(vocab_size, embedding_dim, input_length=max_len))
    model.add(Conv1D(32, (3), activation='relu'))
    model.add(GlobalMaxPooling1D())
    model.add(Dense(64, activation='relu'))
    #model.add(Dense(16, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))
    model.compile(loss='sparse_categorical_crossentropy', 
                  optimizer='adam', metrics=['accuracy'])
                  
    return model, tokenizer, lbl_encoder

def label_encoding(lbl_encoder, training_labels, val_labels):                  
    training_labels = lbl_encoder.transform(training_labels)
    val_labels = lbl_encoder.transform(val_labels)
    
    return training_labels, val_labels

def tokenization(tokenizer, training_sentences, val_sentences):
    #text tokenization
    
    word_index = tokenizer.word_index
    sequences = tokenizer.texts_to_sequences(training_sentences)
    padded_sequences = pad_sequences(sequences, truncating='post', maxlen=max_len)
    sequences = tokenizer.texts_to_sequences(val_sentences)
    val_padded_sequences = pad_sequences(sequences, truncating='post', maxlen=max_len)
    
    return padded_sequences, val_padded_sequences


def training(model, padded_sequences, val_padded_sequences, training_labels, val_labels):
    #training
    early_stop = callbacks.EarlyStopping(monitor='loss',patience=100, restore_best_weights = True)
    epochs = 500
    history = model.fit(padded_sequences, np.array(training_labels), epochs=epochs, validation_data = (val_padded_sequences, np.array(val_labels)), callbacks = [early_stop])
    model.save("model")
    with open('tokenizer.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
    # to save the fitted label encoder
    with open('labelEncoder.pkl', 'wb') as ecn_file:
        pickle.dump(lbl_encoder, ecn_file, protocol=pickle.HIGHEST_PROTOCOL)
    
def evaluate(model, val_padded_sequences, val_labels): 
    loss, acc = model.evaluate(val_padded_sequences, np.array(val_labels), verbose=1)
    print('Test loss: %f' %loss)
    print('Test accuracy: %f' %acc)

if __name__ == '__main__':
    train = True
    training_sentences, training_labels, labels, val_sentences, val_labels, num_classes = loaddata()
    if not train:
        model, tokenizer, lbl_encoder = loadmodel()
    else: 
        model, tokenizer, lbl_encoder = createmodel(training_labels, training_sentences)
    training_labels, val_labels = label_encoding(lbl_encoder, training_labels, val_labels)
    padded_sequences, val_padded_sequences = tokenization(tokenizer, training_sentences, val_sentences)
    
    if not train:
        evaluate(model, val_padded_sequences, val_labels) 
    else:
        training(model, padded_sequences, val_padded_sequences, training_labels, val_labels)
        