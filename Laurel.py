import random
import time
import os 
import string
from gtts import gTTS 
import speech_recognition as sr
import spacy
from Parser import Parser
import numpy as np

class Laurel():

    def __init__(self, recognizer, microphone, limit):
        self.shop_types = ["souvenir stores", "supermarket duty free", "luxury shops", "restaurants", "cafes"]
        self.shop_list = ['mediaworld', 'nike', 'adidas', 'mcdonald']
        self.shop_type_list = ['electronic', 'restaurant', 'clothes', 'cafe', 'hairdresser', 'supermarket']
        self.cities = ["Rome", "London", "Berlin", "Amsterdam", "Dublin", "Madrid", "Milan", "Dublin", "Helsinki", "Oslo", "New York", "Los Angeles"]
        self.items = ["souvenir", "toy", "clothes", "magnet", "perfume"]
        self.shops = [["London souvenirs", "Souvenirs from England", "U.K. souvenirs"], ["Game Stop", "Toys U.K"], \
                    ["Burberry", "Gucci", "Fendi"], ["London souvenirs", "Magnets Love", "U.K. souvenirs"], ["duty free"]]
        self.car_models = ["luxury car"," mini van","utilitarian car"]
        self.items2shops = dict(zip(self.items, self.shops))
        self.recognizer = recognizer
        self.microphone = microphone
        self.limit = limit
        self.parser = Parser()
        
    def recognize_speech_from_mic(self, recognizer, microphone):
        # check that recognizer and microphone arguments are appropriate type
        if not isinstance(recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")

        if not isinstance(microphone, sr.Microphone):
            raise TypeError("`microphone` must be `Microphone` instance")
        # adjust the recognizer sensitivity to ambient noise and record audio
        # from the microphone
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        # set up the response object
        response = {
            "success": True,
            "error": None,
            "transcription": None
        }

        # try recognizing the speech in the recording
        # if a RequestError or UnknownValueError exception is caught,
        #     update the response object accordingly
        try:
            response["transcription"] = recognizer.recognize_google(audio)
        except sr.RequestError:
            # API was unreachable or unresponsive
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            # speech was unintelligible
            response["error"] = "Unable to recognize speech"

        return response
        
    def hear(self):
        for j in range(self.limit):
            print('Speak!')
            guess = self.recognize_speech_from_mic(self.recognizer, self.microphone)
            if guess["transcription"]:
                break
            if not guess["success"]:
                break
            #print("I didn't catch that. What did you say?\n")

            # if there was an error, stop the game
            if guess["error"]:
                #print("ERROR: {}".format(guess["error"]))
                break

        # show the user the transcription
        print("You said: {}".format(guess["transcription"]))
        return guess
        
    def speak(self, sentence):
        language = 'en'
        myobj = gTTS(text=sentence, lang=language, slow=False) 
        myobj.save("audio.mp3") 
        os.system("mpg321.exe audio.mp3")
    
    def greeting(self, sentence):
        self.speak("Hi, how can I help you?")
        return True
    
    def help(self, sentence):
        self.speak("How can I help you?")
        return True
        
    def goodbye(self, sentence):
        answers = ["See you later", "Have a nice day", "Bye!", "Goodbye"]
        choice = random.randint(0,len(answers)-1)
        self.speak(answers[choice])
        return False
        
    def thanks(self, sentence):
        answers = ["Happy to help you!", "My pleasure", "You're welcome!"]
        choice = random.randint(0,len(answers)-1)
        self.speak(answers[choice])
        return False

    def checkStop(self, guess):
        words = self.parser.words(guess)
        candidates = ['stop', 'shut', 'silent', 'quit', 'cancel', 'enough', 'exit', 'exeter']
        return self.parser.shareWords(words, candidates)

    def evaluation(self, sentence):
        answers = ["Ok, I need more details about the evaluation to assist you. Please tell me the kind of property you want to be evalueted.",
                    "I need more details. Please tell me the kind of property you want to be evalueted.",
                    "Is it an apartment or a villa?"]
        choice = random.randint(0,len(answers)-1)
        self.speak(answers[choice])
        guess = None
        while guess is None:
            guess = self.hear()
            guess = guess["transcription"]
            try:
                guess = guess.lower()
                if self.checkStop(guess): return True
                #print(self.parser.words(guess))
                words = self.parser.words(guess)
                candidates = ['apartment', 'villa', 'flat', 'basement', 'attic', 'garden', 'gardens',\
                                'apartments', 'villas', 'flats', 'palaces', 'basements'\
                                'attics', 'loft', 'lofts', 'penthouse', 'penthouses', 'arctic', 'synoptic', 'haptic', 'optic', 'neurotic', 'somatic', 'synaptic', 'article']
                commonWords = self.parser.commonWords(candidates, words)
                if len(commonWords)>=2:
                    self.speak("Please, specify one type only")
                    guess = None
                    continue
                elif self.parser.shareWords(commonWords, ['apartment', 'apartments', 'basement', 'attic', 'basements','attics', 'loft', 'lofts',\
                                                             'penthouse', 'penthouses', 'arctic', 'synoptic', 'haptic', 'optic', 'neurotic', 'somatic', 'article',\
                                                             'flat', 'flats', 'synaptic']):
                    return self.apartmentEvaluation(sentence)
                elif self.parser.shareWords(commonWords, ['villa', 'villas', 'garden', 'gardens']):
                    return self.villaEvaluation(sentence)
                else:
                    guess = None
            except: 
                guess = None
        return True

    def squareMetersHouse(self, type=None):
        squareMeters = None
        #Question 1
        if type=='apartment':
            answers = ["How many square meters?",
                    "How much is big?"]
        else:
            answers = ["How many square meters has your house?",
                        "How much is big your house?"]
        choice = random.randint(0,len(answers)-1)
        self.speak(answers[choice])
        guess = None
        while guess is None:
            guess = self.hear()
            guess = guess["transcription"]
            try:
                guess = guess.lower()
                if self.checkStop(guess): return True
                squareMeters = self.parser.extractNumbers(guess)
                if squareMeters == []:
                    guess = None
                    continue
                squareMeters = sum(squareMeters)
                if squareMeters < 5:
                    self.speak("Probably I didn't get it, it's too small! Can you repeat, please?")
                    guess = None
                    continue
                elif squareMeters <= 20:
                    self.speak("It's a mini house!")
                elif squareMeters <= 80:
                    self.speak("Ok, got it!")
                elif squareMeters <= 130:
                    self.speak("It's a big house")
                elif squareMeters > 130:
                    self.speak("It's huge")
                else:
                    self.speak("Probably I didn't got it, can you repeat, please?")
                    guess = None
                    continue
            except: 
                guess = None
        return squareMeters

    def squareMetersGarden(self):
        squareMeters = None
        #Question 1
        answers = ["Ok, how many square meters is your garden?",
                    "Ok, how much is big your garden?"]
        choice = random.randint(0,len(answers)-1)
        self.speak(answers[choice])
        guess = None
        while guess is None:
            guess = self.hear()
            guess = guess["transcription"]
            try:
                guess = guess.lower()
                if self.checkStop(guess): return True
                squareMeters = self.parser.extractNumbers(guess)
                if squareMeters == []:
                    guess = None
                    continue
                squareMeters = sum(squareMeters)
                if squareMeters < 3:
                    self.speak("Probably I didn't get it, it's too small! Can you repeat, please?")
                    guess = None
                    continue
                elif squareMeters <= 15:
                    self.speak("It's a mini garden!")
                elif squareMeters <= 95:
                    self.speak("Ok, got it!")
                elif squareMeters <= 200:
                    self.speak("It's a big garden")
                elif squareMeters > 200:
                    self.speak("It's huge")
                else:
                    self.speak("Probably I didn't got it, can you repeat, please?")
                    guess = None
                    continue
            except: 
                guess = None
        return squareMeters

    def isCorrect(self, sentence):
        yes1 = ['yeah', 'yes', 'correct', 'positive', 'right', 'ok', 'okay', 'proceed']
        no1 = ['no', 'nope', 'not' 'negative', 'wrong', 'neither', 'mistake']
        yes2 = ['it is']
        no2 = ["it isn't", "not correct", "no correct", "not right", "not ok", "not okay"]
        words = self.parser.words(sentence)
        wordPairs = self.parser.makePairs(words)
        cwYes1 = len(self.parser.commonWords(yes1, words))
        cwYes2 = len(self.parser.commonWords(yes2, wordPairs))
        cwNo1 = len(self.parser.commonWords(no1, words))
        cwNo2 = len(self.parser.commonWords(no2, wordPairs))
        if cwNo2!=0:
            return False
        if cwNo1+cwYes1>max(cwNo1, cwYes1):
            return None
        if cwNo1!=0:
            return False
        if cwYes1!=0:
            return True
        if cwYes2!=0:
            return True
        return None

    def position(self):
        #Question 2
        self.speak("Is it near the center?")
        guess = None
        postion = None
        while guess is None:
            guess = self.hear()
            guess = guess["transcription"]
            try:
                guess = guess.lower()
                if self.checkStop(guess): return True
                words = self.parser.words(guess)
                groupCenter = ['yeah', 'yes', 'center', 'central', 'kind', 'almost', 'quite', 'near']
                #groupSemiPeripheral = ['middle', 'semi-suburbs', 'semi-peripheral', 'semi-periphery']
                groupPeripheral = ['nope', 'not', 'no', 'peripheral', 'suburbs', 'periphery', 'outskirts', 'distant', 'far', 'away']
                commonWordsCenterLen = len(self.parser.commonWords(groupCenter, words))
                #commonWordsSemiPeripheralLen = len(self.parser.commonWords(groupSemiPeripheral, words))
                commonWordsPeripheralLen = len(self.parser.commonWords(groupPeripheral, words))
                if commonWordsCenterLen+commonWordsPeripheralLen>\
                max(commonWordsCenterLen, commonWordsPeripheralLen):
                    self.speak("Please, give me a unique answer")
                    guess = None
                    continue
                elif commonWordsCenterLen>=1:
                    self.speak("Nice, it's good for the evaluation")
                    position = 'the center'
                #elif commonWordsSemiPeripheralLen>=1:
                    #self.speak("Ok")
                    #position = 'semi-perifery'
                elif commonWordsPeripheralLen>=1:
                    self.speak("That's not so good for the evaluation")
                    position = 'periphery'
                else:
                    guess = None
                    continue
            except: 
                guess = None
        return position

    def floor(self):
        #Question 3
        self.speak("Is it an attic or a basement?")
        guess = None
        floor = None
        while guess is None:
            guess = self.hear()['transcription']
            try:
                guess = guess.lower()
                if self.checkStop(guess): return True
                words = self.parser.words(guess)
                attic = ['attic', 'last', 'penthouse', 'loft', 'arctic', 'synoptic', 'haptic', 'optic', 'neurotic', 'somatic', 'synaptic', 'article']
                basement = ['basement', 'minus', 'garage', 'underground']
                cwAttic = len(self.parser.commonWords(attic, words))
                cwBasement = len(self.parser.commonWords(basement, words))

                if cwAttic+cwBasement>max(cwAttic, cwBasement):
                    self.speak("Please, give me a unique answer")
                    guess = None
                    continue
                elif cwAttic!=0:
                    floor = 'attic'
                    self.speak("Oh very good!")
                elif cwBasement!=0:
                    floor = 'basement'
                    self.speak("Okey.")
                else:
                    correct = self.isCorrect(guess)
                    if correct:
                        self.speak("Specify if it is an attic or a basement")
                        guess = None
                        continue
                    elif correct == False:
                        floor = 'normal'
                        self.speak("Got it.")
                    else:
                        guess = None
                        continue
            except:
                guess = None
        return floor

    def nBathrooms(self):
        #Question 4
        self.speak("How many bathrooms are present?")
        guess = None
        nBathrooms = None
        while guess is None:
            guess = self.hear()
            guess = guess["transcription"]
            try:
                guess = guess.lower()
                if self.checkStop(guess): return True
                nBathrooms = self.parser.extractNumbers(guess)

                if nBathrooms == []:
                    guess = None
                    continue
                nBathrooms = sum(nBathrooms)
                if nBathrooms <=0:
                    self.speak("Probably I didn't get it, it's impossible. Can you repeat, please?")
                    guess = None
                    continue
                elif nBathrooms == 1:
                    self.speak("Ok, it's standard.")
                elif nBathrooms == 2:
                    self.speak("Ok, good!")
                elif nBathrooms == 3:
                    self.speak("That's great, only few houses has 3 bathrooms!")
                elif nBathrooms >= 4:
                    self.speak("Wow, fantastic! You will be full of money!")
                else:
                    self.speak("Probably I didn't got it, can you repeat, please?")
                    guess = None
                    continue
            except: 
                guess = None
        return nBathrooms

    def apartmentEvaluation(self, sentence, wrong=None, squareMeters=None, position=None, floor=None, nBathrooms=None):

        if wrong is None or wrong == 'squareMeters':
            squareMeters = self.squareMetersHouse('apartment')
            if squareMeters is True: return True

        if wrong is None or wrong == 'position':
            position = self.position()
            if position is True: return True

        if wrong is None:
            self.speak("Let's continue!")

        if wrong is None or wrong == 'floor':
            floor = self.floor()
            if floor is True: return True

        if wrong is None:
            self.speak("Last question!")

        if wrong is None or wrong == 'nBathrooms':
            nBathrooms = self.nBathrooms()
            if nBathrooms is True: return True

        sentenceToTell = "So, let's do a summary! Your apartment is in "+position

        if floor == 'attic':
            sentenceToTell += ", it's an attic"
        if floor == 'basement':
            sentenceToTell += ", it's a basement"

        sentenceToTell += ", it is "+str(squareMeters)+" square meters large and it has "+str(nBathrooms)+\
                            " bathrooms. Is it correct?"
        self.speak(sentenceToTell)
        guess = None
        while guess is None:
            guess = self.hear()["transcription"]
            try:
                guess = guess.lower()
                if self.checkStop(guess): return True
                correctness = self.isCorrect(guess)
                if correctness == None:
                    self.speak("Please, give me a unique answer")
                    guess = None
                    continue
                elif correctness == True:
                    evaluation = squareMeters*3000

                    if position == 'center': evaluation *= 2
                    elif position == 'periphery': evaluation *= 1

                    if floor == 'attic': evaluation *= 1.3
                    elif floor == 'basement': evaluation *= 0.67
                    else: evaluation *= 1

                    evaluation += (nBathrooms-1)*30000

                    evaluation = int(round(evaluation, -3))
                    sentenceToTell = "Very good, my personal evaluation for your apartment is around "+str(evaluation)+\
                                    " Euros, we could publish an announcement asking "+str(int(round(evaluation*1.15, -3)))+\
                                    " Euros that is 15 percent higher than his real value. If you want we can publish an announcement, do you agree?"
                    self.speak(sentenceToTell)
                    guess = None
                    while guess is None:
                        guess = self.hear()["transcription"]
                        try:
                            guess = guess.lower()
                            if self.checkStop(guess): return True
                            correctness = self.isCorrect(guess)
                            if correctness == None:
                                self.speak("Please, give me a unique answer")
                                guess = None
                                continue
                            elif correctness == True:
                                self.speak("Great! We will call you if we receive a bid.")
                                self.speak("If I can do something else for you, just ask me.")
                            else:
                                self.speak("Ok, no problem, when you want you can call us.")
                                self.speak("If I can do something else for you, just ask me.")
                        except:
                            guess = None
                else:
                    self.speak("What is wrong?")
                    guess = None
                    while guess is None:
                        guess = self.hear()["transcription"]
                        try:
                            guess = guess.lower()
                            if self.checkStop(guess): return True
                            words = self.parser.words(guess)
                            squareMetersCand = ['square', 'meters', 'metres', 'meter', 'metre', 'dimensions', 'dimension',\
                                            'size', 'big', 'small', 'squared', 'squares', 'area', 'surface', 'walkable'\
                                            'metering', 'footage', 'footprint', 'metrification', 'metrature']
                            positionCand = ['position', 'place', 'where', 'site', 'zone' 'location', 'center', 'central', 'peripheral',\
                                         'suburbs', 'suburbs', 'periphery', 'outskirts', 'semi-suburbs', 'semi-suburbs']
                            floorCand = ['attic', 'last', 'basement', 'minus', 'garage', 'ground', 'underground', 'penthouse', 'loft',\
                                         'arctic', 'synoptic', 'haptic', 'optic', 'neurotic', 'somatic', 'synaptic', 'article']
                            nBathroomsCand = ['bathrooms', 'restroom', 'bath', 'bathroom', 'restrooms', 'room', 'rooms', 'paths']
                            cwSquareMeters = len(self.parser.commonWords(squareMetersCand, words))
                            cwPosition = len(self.parser.commonWords(positionCand, words))
                            cwFloor = len(self.parser.commonWords(floorCand, words))
                            cwNBathrooms = len(self.parser.commonWords(nBathroomsCand, words))

                            if cwSquareMeters+cwPosition+cwFloor+cwNBathrooms>max(cwSquareMeters, cwPosition, cwFloor, cwNBathrooms):
                                self.speak("Please, give me a unique answer")
                                guess = None
                                continue
                            elif cwSquareMeters!=0:
                                self.speak("Oh, I'm sorry, I've missunderstood")
                                return self.apartmentEvaluation(None, wrong='squareMeters', squareMeters=squareMeters, position=position,\
                                                                floor=floor, nBathrooms=nBathrooms)
                            elif cwPosition!=0:
                                self.speak("Oh, I'm sorry, I've missunderstood")
                                return self.apartmentEvaluation(None, wrong='position', squareMeters=squareMeters, position=position,\
                                                                floor=floor, nBathrooms=nBathrooms)
                            elif cwFloor!=0:
                                self.speak("Oh, I'm sorry, I've missunderstood")
                                return self.apartmentEvaluation(None, wrong='floor', squareMeters=squareMeters, position=position,\
                                                                floor=floor, nBathrooms=nBathrooms)
                            elif cwNBathrooms!=0:
                                self.speak("Oh, I'm sorry, I've missunderstood")
                                return self.apartmentEvaluation(None, wrong='nBathrooms', squareMeters=squareMeters, position=position,\
                                                                floor=floor, nBathrooms=nBathrooms)
                            else:
                                guess = None
                                continue
                        except:
                            guess = None
            except:
                guess = None

        return True

    def villaEvaluation(self, sentence, wrong=None, squareMetersGarden=None, squareMeters=None, position=None, nBathrooms=None):

        if wrong is None or wrong == 'squareMeters':
            squareMetersGarden = self.squareMetersGarden()
            if squareMetersGarden is True: return True

        if wrong is None or wrong == 'squareMeters':
            squareMeters = self.squareMetersHouse()
            if squareMeters is True: return True

        if wrong is None or wrong == 'position':
            position = self.position()
            if position is True: return True

        if wrong is None:
            self.speak("Let's continue!")

        if wrong is None:
            self.speak("Last question!")

        if wrong is None or wrong == 'nBathrooms':
            nBathrooms = self.nBathrooms()
            if nBathrooms is True: return True

        sentenceToTell = "So, let's do a summary! Your villa is in "+position

        sentenceToTell += ", it is "+str(squareMeters)+" square meters large and it has a garden of about "+str(squareMetersGarden)+\
                            ", finally, it has "+str(nBathrooms)+" bathrooms. Is it correct?"
        self.speak(sentenceToTell)
        guess = None
        while guess is None:
            guess = self.hear()["transcription"]
            try:
                guess = guess.lower()
                if self.checkStop(guess): return True
                correctness = self.isCorrect(guess)
                if correctness == None:
                    self.speak("Please, give me a unique answer")
                    guess = None
                    continue
                elif correctness == True:
                    evaluation = squareMeters*3000 + squareMetersGarden*500

                    if position == 'center': evaluation *= 2
                    elif position == 'periphery': evaluation *= 1

                    else: evaluation *= 1

                    evaluation += (nBathrooms-1)*30000

                    evaluation = int(round(evaluation, -3))
                    sentenceToTell = "Very good, my personal evaluation for your villa is around "+str(evaluation)+\
                                    " Euros, we could publish an announcement asking "+str(int(round(evaluation*1.15, -3)))+\
                                    " Euros that is 15 percent higher than his real value. If you want we can publish an announcement, do you agree?"
                    self.speak(sentenceToTell)
                    guess = None
                    while guess is None:
                        guess = self.hear()["transcription"]
                        try:
                            guess = guess.lower()
                            if self.checkStop(guess): return True
                            correctness = self.isCorrect(guess)
                            if correctness == None:
                                self.speak("Please, give me a unique answer")
                                guess = None
                                continue
                            elif correctness == True:
                                self.speak("Great! We will call you if we receive a bid.")
                                self.speak("If I can do something else for you, just ask me.")
                            else:
                                self.speak("Ok, no problem, when you want you can call us.")
                                self.speak("If I can do something else for you, just ask me.")
                        except:
                            guess = None
                else:
                    self.speak("What is wrong?")
                    guess = None
                    while guess is None:
                        guess = self.hear()["transcription"]
                        try:
                            guess = guess.lower()
                            if self.checkStop(guess): return True
                            words = self.parser.words(guess)
                            squareMetersCand = ['square', 'meters', 'metres', 'meter', 'metre', 'dimensions', 'dimension',\
                                            'size', 'big', 'small', 'squared', 'squares', 'area', 'surface', 'walkable'\
                                            'metering', 'footage', 'footprint', 'metrification', 'metrature', 'garden', 'green',\
                                            'terrain', 'yard']
                            positionCand = ['position', 'place', 'where', 'site', 'zone' 'location', 'center', 'central', 'peripheral',\
                                         'suburbs', 'suburbs', 'periphery', 'outskirts', 'semi-suburbs', 'semi-suburbs']
                            nBathroomsCand = ['bathrooms', 'restroom', 'bath', 'bathroom', 'restrooms', 'room', 'rooms', 'paths']
                            cwSquareMeters = len(self.parser.commonWords(squareMetersCand, words))
                            cwPosition = len(self.parser.commonWords(positionCand, words))
                            cwNBathrooms = len(self.parser.commonWords(nBathroomsCand, words))

                            if cwSquareMeters+cwPosition+cwNBathrooms>max(cwSquareMeters, cwPosition, cwNBathrooms):
                                self.speak("Please, give me a unique answer")
                                guess = None
                                continue
                            elif cwSquareMeters!=0:
                                self.speak("Oh, I'm sorry, I've missunderstood")
                                return self.apartmentEvaluation(None, wrong='squareMeters', squareMetersGarden=squareMetersGarden, squareMeters=squareMeters,\
                                                                position=position, nBathrooms=nBathrooms)
                            elif cwPosition!=0:
                                self.speak("Oh, I'm sorry, I've missunderstood")
                                return self.apartmentEvaluation(None, wrong='position', squareMetersGarden=squareMetersGarden, squareMeters=squareMeters,\
                                                                position=position, nBathrooms=nBathrooms)
                            elif cwNBathrooms!=0:
                                self.speak("Oh, I'm sorry, I've missunderstood")
                                return self.apartmentEvaluation(None, wrong='nBathrooms', squareMetersGarden=squareMetersGarden, squareMeters=squareMeters,\
                                                                position=position, nBathrooms=nBathrooms)
                            else:
                                guess = None
                                continue
                        except:
                            guess = None
            except:
                guess = None

        return True

    def housesAvailability(self, sentence):
        answers = ["There are some houses available, how much do you want to spend?",
                    "There are some options depending on how much money you can spend. How much is it?",
                    "How much do you want to spend?"]
        choice = random.randint(0, len(answers)-1)
        self.speak(answers[choice])
        guess = None
        while guess is None:
            guess = self.hear()
            guess = guess["transcription"]
            try:
                guess = guess.replace("€", "")
                guess = guess.replace("$", "")
                guess = guess.replace(",", "")
                guess = guess.replace(" millions", "000000")
                guess = guess.replace(" million", "000000")
                guess = guess.replace(" median", "000000")
                guess = guess.lower()
                if self.checkStop(guess): return True
                print(guess)
                budget = self.parser.extractNumbers(guess)
                print(budget)
                if len(budget)!=0:
                    budget = int(round(sum(budget)/len(budget), -4))
                    print(budget)
                    if budget<=10000:
                        self.speak("Probably I didn't get it, it's impossible at that price! Can you repeat, please?")
                        guess = None
                        continue
                    numHouses = random.randint(0, 2)
                    print(numHouses)
                    if numHouses == 0:
                        answer = "I'm sorry but we don't have houses in line with your budget. Come back later, you may be lucky"
                    elif numHouses == 1:
                        answer = "We have an house which costs "+str(int(round(budget*1.1)))+" Euros, which is a little bit more than your budget."+\
                                    "If you are still interested, when you want you can schedule an appointment with an our agent."
                    elif numHouses == 2:
                        answer = "We have two houses which cost "+str(int(round(budget*0.85)))+" Euros and "+str(int(round(budget*1.1)))+" Euros which is around your budget."+\
                                    "If you are interested, when you want you can schedule an appointment with an our agent."
                    self.speak(answer)
                else:
                    guess = None
                    continue

            except:
                guess = None
        return True


    def appointment(self, sentence):
        self.speak("Yes, we can arrange an appointment with an our agent. When do you prefer?")
        guess = None
        while guess is None:
            try:
                guess = self.hear()["transcription"].lower()
                if self.checkStop(guess): return True
                guess = guess.replace("about ", "")
                guess = guess.replace(" about", "")
                ent = self.parser.entities(guess)
                guess = ent["DATE"][0]
                when = guess
                if when == 'yesterday':
                    guess = None
                    continue
                choice = random.randint(0, 1)
                if choice == 0:
                    self.speak("I'm sorry, but for "+ when + "all our agents are unavailable. Please tell me another date.")
                    guess = None
                    continue
                else:
                    self.speak("Ok, I scheduled it for " + when + " with " + random.choice(['John', 'Mark', 'Mattew', 'Luke', 'Mary', 'Joseph']))
            except:
                guess = None

        return True
