import random
import time
import os 
import string
from gtts import gTTS 
import speech_recognition as sr
import spacy
from Parser import Parser
import numpy as np


#["Please provide us your complaint in order to assist you", "Please mention your complaint, we will reach you and sorry for any inconvenience caused"]

'''

{"tag": "shoptypes",
	"patterns": ["which kind of shops are there in the airport", "which types of shops can I find in the airport", "what kind of shops are there in the airport"]
	},
{"tag": "about",
     "patterns": ["Who are you?", "What are you?", "Who you are?" ]
    },
    {"tag": "name",
    "patterns": ["what is your name", "what should I call you", "whats your name?"]
    },
    
    def shops(self, sentence):
        rnd1 = random.randint(0,len(self.shop_list)-1)
        rnd2 = random.randint(0,len(self.shop_list)-1)
        while rnd1 == rnd2:
            rnd2 = random.randint(0,len(self.shop_list)-1)
        print('Some of the shops you can find here are the followings: ' +  self.shop_list[rnd1] + ', ' + self.shop_list[rnd2])
        self.speak('Some of the shops you can find here are the followings: ' +  self.shop_list[rnd1] + ', ' + self.shop_list[rnd2])
        return True
    
    def shoptypes(self, sentence):
        rnd1 = random.randint(0,len(self.shop_types)-1)
        rnd2 = random.randint(0,len(self.shop_types)-1)
        while rnd1 == rnd2:
            rnd2 = random.randint(0,len(self.shop_types)-1)
        print('For example you can find these types of shops: ' +  self.shop_types[rnd1] + ', ' + shop_types[rnd2])
        self.speak('For example you can find these types of shops: ' +  shop_types[rnd1] + ', ' + shop_types[rnd2])
        return True
'''

#sistemare la conferma della prenotazione volo

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
        print("Hi, how can I help you?")
        self.speak("Hi, how can I help you?")
        return True
    
    def help(self, sentence):
        self.speak("How can I help you?")
        return True
        
    def goodbye(self, sentence):
        answers = ["See you later", "Have a nice day", "Bye!", "Bye! Come back again"]
        choice = random.randint(0,len(answers)-1)
        self.speak(answers[choice])
        return False
        
    def thanks(self, sentence):
        answers = ["Happy to help!", "Any time!", "My pleasure", "You're most welcome!"]
        choice = random.randint(0,len(answers)-1)
        self.speak(answers[choice])
        return False
    
    def complaint(self, sentence):
        answers = ["Please provide us your complaint in order to assist you", "Please mention your complaint, we will reach you and sorry for any inconvenience caused"]
        choice = random.randint(0,len(answers)-1)
        self.speak(answers[choice])
        return False

    def evaluation(self, sentence):
        answers = ["Ok, I need more details about the evaluation to assist you. Please tell me the kind of property you want to be evalueted.",
                    "I need more details. Please tell me the kind of property you want to be evalueted.",
                    "Is it an apartment, a garage, a villa or a land?"]
        choice = random.randint(0,len(answers)-1)
        self.speak(answers[choice])
        guess = None
        while guess is None:
            guess = self.hear()
            guess = guess["transcription"]
            try:
                guess = guess.lower()
                #print(self.parser.words(guess))
                words = self.parser.words(guess)
                candidates = ['apartment', 'garage', 'villa', 'land', 'box', 'flat', 'palace', 'hotel', 'terrain', 'basement', 'attic',\
                                'apartments', 'garages', 'villas', 'lands', 'boxes', 'flats', 'palaces', 'hotels', 'terrains', 'basements',\
                                'attics', 'loft', 'lofts', 'penthouse', 'penthouses', 'arctic', 'synoptic', 'haptic', 'optic', 'neurotic', 'somatic', 'synaptic']
                commonWords = self.parser.commonWords(candidates, words)
                if len(commonWords)>=2:
                    self.speak("Please, specify one type only")
                    guess = None
                    continue
                elif self.parser.shareWords(commonWords, ['apartment', 'apartments', 'basement', 'attic', 'basements','attics', 'loft', 'lofts',\
                                                             'penthouse', 'penthouses', 'arctic', 'synoptic', 'haptic', 'optic', 'neurotic', 'somatic', 'synaptic']):
                    return self.apartmentEvaluation(sentence)
                else:
                    guess = None
            except: 
                guess = None
        return True

    def squareMetersApartment(self):
        squareMeters = None
        #Question 1
        answers = ["Ok, how many square meters?",
                    "Ok, how much is big?"]
        choice = random.randint(0,len(answers)-1)
        self.speak(answers[choice])
        guess = None
        while guess is None:
            guess = self.hear()
            guess = guess["transcription"]
            try:
                guess = guess.lower()
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
                    self.speak("It's a mini apartment!")
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

    def isCorrect(self, sentence):
        yes1 = ['yeah', 'yes', 'correct', 'positive', 'right', 'ok', 'okay']
        no1 = ['no', 'nope', 'not' 'negative', 'wrong', "neither"]
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

    def apartmentEvaluation(self, sentence, wrong=None, squareMeters=None, position=None, floor=None, nBathrooms=None):

        if wrong is None or wrong == 'squareMeters':
            squareMeters = self.squareMetersApartment()

        if wrong is None or wrong == 'position':
            #Question 2
            self.speak("Is it near the center?")
            guess = None
            while guess is None:
                guess = self.hear()
                guess = guess["transcription"]
                try:
                    guess = guess.lower()
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

        if wrong is None:
            self.speak("Let's continue!")

        if wrong is None or wrong == 'floor':
            #Question 3
            self.speak("Is it an attic or a basement?")
            guess = None
            while guess is None:
                guess = self.hear()['transcription']
                try:
                    guess = guess.lower()
                    words = self.parser.words(guess)
                    attic = ['attic', 'last', 'penthouse', 'loft', 'arctic', 'synoptic', 'haptic', 'optic', 'neurotic', 'somatic', 'synaptic']
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

        if wrong is None:
            self.speak("Last question!")

        if wrong is None or wrong == 'nBathrooms':
            #Question 4
            self.speak("How many bathrooms are present?")
            guess = None
            while guess is None:
                guess = self.hear()
                guess = guess["transcription"]
                try:
                    guess = guess.lower()
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

                    evaluation = round(evaluation)
                    sentenceToTell = "Very good, my personal evaluation for your apartment is around "+str(evaluation)+\
                                    " Euros, we could publish an announcement asking "+str(round(evaluation*1.15))+\
                                    " Euros that is 15 percent higher than his real value. If you want we can publish an announcement, do you agree?"
                    self.speak(sentenceToTell)
                    guess = None
                    while guess is None:
                        guess = self.hear()["transcription"]
                        try:
                            guess = guess.lower()
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
                                self.speak("If I can do someting else for you, just ask me.")
                        except:
                            guess = None
                else:
                    self.speak("What is wrong?")
                    guess = None
                    while guess is None:
                        guess = self.hear()["transcription"]
                        try:
                            guess = guess.lower()
                            words = self.parser.words(guess)
                            squareMetersCand = ['square', 'meters', 'metres', 'meter', 'metre', 'dimensions', 'dimension',\
                                            'size', 'big', 'small', 'squared', 'squares', 'area', 'surface', 'walkable'\
                                            'metering', 'footage', 'footprint', 'metrification', 'metrature']
                            positionCand = ['position', 'place', 'where', 'site', 'zone' 'location', 'center', 'central', 'peripheral',\
                                         'suburbs', 'suburbs', 'periphery', 'outskirts', 'semi-suburbs', 'semi-suburbs']
                            floorCand = ['attic', 'last', 'basement', 'minus', 'garage', 'ground', 'underground', 'penthouse', 'loft',\
                                         'arctic', 'synoptic', 'haptic', 'optic', 'neurotic', 'somatic', 'synaptic']
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


    
    def shoppresence(self, sentence):
        complobj = None
        chunks = self.parser.noun_chunks(sentence)
        complobj = chunks['dobj'] if 'dobj' in chunks.keys() else chunks['attr']
        while complobj is None:
            self.speak("I've not understood. Please repeat.")
            guess = self.hear()
            sentence = guess["transcription"]
            chunks = self.parser.noun_chunks(sentence)
            complobj = chunks['dobj'] if 'dobj' in chunks.keys() else chunks['attr']
        
        complobj = complobj.lower()
        here = False
        for string in self.shop_list:
            if complobj in string or string in complobj:
                here = True
        if not here:
            for string in self.shop_type_list:
                if complobj in string or string in complobj:
                    here = True
        if here:
            self.speak("Yes, you can find " + complobj + ' in our airport!')
        else:
            rnd1 = random.randint(0,len(self.shop_type_list)-1)
            rnd2 = random.randint(0,len(self.shop_type_list)-1)
            while rnd1 == rnd2:
                rnd2 = random.randint(0,len(self.shop_type_list)-1)
            self.speak("No, I'm really sorry about this. But you can find some other very interesting shops like: "+  self.shop_type_list[rnd1] + ', ' + self.shop_type_list[rnd2])
        return True  
        
        
    def flightconf(self, departure, destination, when):
        conf = None
        while conf is None:
            guess = self.hear()
            conf = guess["transcription"]
        conf = conf.lower()
        words = self.parser.words(conf)
        if "no" in words:
            self.speak("okay, I'm here for you when you want")
        elif "yes" in words:
            self.speak("okay, I'm booking a flight for you from " + str(departure) + " to " + str(destination) + " for " + str(when))
        else:
            self.speak("I did not get it, sorry, can you please repeat?")
            self.flightconf(departure, destination, when)
    
    def buildgatecode(self):
        letter = random.choice(string.ascii_letters)
        number = random.randint(10, 99)
        return letter + str(number)
    
    def checkflightcode(self, code):
        if len(code) is not 6:
            return False
        else:
            for i in range(len(code)):
                if i is 1 or i is 0:
                    if not code[i].isalpha():
                        return False
                else:
                    if not code[i].isdigit:
                        return False
        return True
        
    def flightgate(self, sentence):
        self.speak("To avoid any mistake looking for the gate of your flight, please tell me only the code of your flight with clear voice")
        guess = None
        isValid = False
        while guess is None or not isValid:
            guess = self.hear()
            guess = guess["transcription"]
            if self.checkflightcode(guess):
                isValid = True
            else:
                self.speak("That is not a valid code. Try again please.")
        code = guess.lower()
        gatecode = self.buildgatecode()
        self.speak("The gate of yout flight " + code.replace(" ", "") + "is " + gatecode)
        return True
       
    def flightcheckin(self,sentence):
        self.speak("To avoid any mistake looking for the terminal of your flight, please tell me only the code of your flight with clear voice")
        guess = None
        isValid = False
        while guess is None or not isValid:
            guess = self.hear()
            guess = guess["transcription"]
            if self.checkflightcode(guess):
                isValid = True
            else:
                self.speak("That is not a valid code. Try again please.")
        code = guess.lower()
        terminalnum = random.randint(1, 10)
        self.speak("The terminal for your flight " + code.replace(" ", "") + " is the number " + str(terminalnum) +". There you can check in for the flight. Enjoy it.")
        return True
        
    def flightinfo(self, sentence):
        self.speak("To avoid any mistake looking for the status of your flight, please tell me only the code of your flight with clear voice")
        guess = None
        isValid = False
        while guess is None or not isValid:
            guess = self.hear()
            guess = guess["transcription"]
            if self.checkflightcode(guess):
                isValid = True
            else:
                self.speak("That is not a valid code. Try again please.")
        code = guess.lower()
        
        rnd1 = random.randint(0,len(self.shop_type_list)-1)
        rnd2 = random.randint(0,len(self.shop_type_list)-1)
        while rnd1 == rnd2:
            rnd2 = random.randint(0,len(self.shop_type_list)-1)
        departure = self.cities[rnd1]
        destination = self.cities[rnd2]
        
        delays = ["15 minutes", "30 minutes", "1 hour", "2 hours", "4 hours"]
        status = ["in time", "cancelled", "delayed"]
        rnd = random.randint(0,len(status)-1)
        rndstatus = status[rnd]
        
        randomtime = random. randint(8, 22)
        
        s = "Your flight with code " + code.replace(" ", "") + "from " + departure + " to " + destination +"is " + rndstatus
        
        if rndstatus == "delayed":
            rnd = random.randint(0,len(delays)-1)
            rnddelay = delays[rnd]
            statussentence = " of " + rnddelay + " .I'm sorry"
        elif rndstatus == "in time":
            statussentence = " .So it will leave at " + str(randomtime) + "o'clock."
        else:
            statussentence = " I'm really sorry about this."
            
        self.speak(s+statussentence)
        return True
    
    def findcities(self, children, entities, prep):
        city = None
        print(entities)
        if prep in children:
            try:
                city = children[prep][0] if children[prep][0] in entities["GPE"] else None
                print(city)
            except:
                return city
        return city
    
    def flight(self, sentence):
        children= self.parser.parse(sentence)
        entities = self.parser.entities(sentence)
        departure = self.findcities(children, entities, 'from')
        destination = self.findcities(children, entities,'to')
        while departure is None:
            self.speak("from where do you want to leave?")
            guess = self.hear()
            try:
                entities = self.parser.entities(guess["transcription"])
                departure = entities["GPE"]
            except:
                departure = None
        while destination is None:
            self.speak("where do you want to go?")
            guess = self.hear()
            try:
                entities = self.parser.entities(guess["transcription"])
                destination = entities["GPE"]
            except:
                destination = None
        '''
        if 'for' in children:
            when = children['for'][0]
        '''
        if 'DATE' in entities.keys():
            when = entities["DATE"]
        else:    
            self.speak("when do you want to leave?")
            guess = None
            while guess is None:
                guess = self.hear()
                guess = guess["transcription"]
                try:
                    ent = self.parser.entities(guess)
                    guess = ent["DATE"]
                except: 
                    guess = None
            when = guess
         
        return departure, destination, when
        
    def flightbooking(self, sentence):
        randomprice = random.randint(20,400)
        randomtime = random. randint(8, 22)
        randomexistence = random.randint(0,1)
        
        departure, destination, when = self.flight(sentence)
        if randomexistence == 0:
            self.speak("I'm really sorry about this, but there is no flight like this")
        else:
            self.speak("Yes, there is a flight from " + str(departure) + " to " + str(destination) + " for " + str(when) + ". It's cost is " + str(randomprice) + "euros " +\
            "and it leaves at " + str(randomtime) + "o'clock. Do you want me to book it for you?")
            self.flightconf(departure, destination, when)
        return True
        
    def disablepeople(self, sentence):
        self.speak("Dear customer, we offer any kind of assistance for people with disabilities. \
        The airport offers assistance for any displacement in the airport, help for flights information and for luggage displacement\
        . Which kind of assistance do you need?")
        
        guess = None
        while guess is None:
            guess = self.hear()
            guess = guess["transcription"]
        assistance_needed = guess
        self.speak("When do you need it?")
        guess = None
        while guess is None:
            guess = self.hear()
            guess = guess["transcription"]
            try:
                ent = self.parser.entities(guess)
                guess = ent["DATE"]
            except: 
                guess = None
        when = guess
        self.speak("Perfect, one of our dependents will be available for you " + when + "for the assistance service you have chosen: "+ assistance_needed)
        return True
        
    def wheretobuy(self, sentence):
        complobj = None
        chunks = self.parser.noun_chunks(sentence)
        print (chunks)
        complobj = chunks['dobj'] if 'dobj' in chunks.keys() else None
        while complobj is None:
            self.speak("I've not understood. Please repeat.")
            guess = self.hear()
            sentence = guess["transcription"]
            chunks = self.parser.noun_chunks(sentence)
            complobj = chunks['dobj'] if 'dobj' in chunks.keys() else None
        
        soldhere = False 
        
        for string in self.items:
            if string in complobj or complobj in string:
                soldhere = True
                break
            
        if soldhere:
            str = ""
            for i in self.items2shops[string]:
                str = str + i
                str = str + ", "
            self.speak("You can buy " + complobj + "in the following shops: "+ str)
            
        else:
            self.speak("I'm really sorry, there are no shops selling what you are looking for")
        return True
    
    def rentacar(self,sentence):
        self.speak("Yes, which kind of car do you need? The followings are the models we have available: luxury car, mini van, utilitarian car.")
        guess = None
        while guess is None or guess not in self.car_models:
            guess = self.hear()
            guess = guess["transcription"]
            if guess not in self.car_models:
                self.speak("this model is not available, sorry, try with another one")
        car_model = guess
        isValid = False
        self.speak("For how many days do you need it?. Please specify the exact number of days")
        guess = None
        while guess is None:
            guess = self.hear()
            guess = guess["transcription"]
            try:
                ent = self.parser.entities(guess)
                guess = ent["DATE"]
            except: 
                guess = None
        num_days = guess
        
        self.speak("Ok, you have rent a " + car_model + " for "+ num_days)
        
        return True

    def bookhotel(self, sentence):
        self.speak("I can suggest you a wonderful hotel near the airport. The Royal hotel. Do you want me to book a room there for you?")
        guess = None
        while guess is None:
            guess = self.hear()
            guess = guess["transcription"]
        confirm = guess
        if "yes" in confirm or "Yes" in confirm:
            self.speak("For how many days do you need it?. Please specify the exact number of days")
            guess = None
            while guess is None:
                guess = self.hear()
                guess = guess["transcription"]
                try:
                    ent = self.parser.entities(guess)
                    guess = ent["DATE"]
                except: 
                    guess = None
            num_days = guess
            
            self.speak("Ok, I have booked for you a room in the Royal hotel for" + num_days)
        else:
            self.speak("Ok, I'm here for you when you want")
        return True
        
    def yes(self, sentence):
        self.speak("Okay! Done")
        
    def no(self, sentence):
        self.speak("I'm here for you when you want!")
        
    def notunderstood(self):
        self.speak("I have not understood, can you please repeat?")

print(Laurel(None, None, None).isCorrect("has it told you already"))