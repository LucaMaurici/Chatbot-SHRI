import spacy
from word2number import w2n

class Parser():

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
    
    def noun_chunks(self, sentence):
        chunck_dict = {}
        sentence = self.nlp(sentence)
        for chunk in sentence.noun_chunks:
            print(chunk)
            if chunk.root.dep_ not in chunck_dict.keys():
                chunck_dict[chunk.root.dep_] = list()
            chunck_dict[chunk.root.dep_].append(chunk.text)
        return chunck_dict

    def noun_chunksTexts(self, sentence):
        sentence = self.nlp(sentence)
        chunck_list = list()
        for chunk in sentence.noun_chunks:
            chunck_list.append(chunk.text)
        return chunck_list

    def noun_chunksDependences(self, sentence):
        sentence = self.nlp(sentence)
        chunck_list = list()
        for chunk in sentence.noun_chunks:
            chunck_list.append(chunk.text)
        return chunck_list
        
    def entities(self, sentence):
        sentence = self.nlp(sentence)
        labels = []
        for ent in sentence.ents:
            labels.append(ent.label_)
        labels = list(set(labels))
        values = []
        for i in range(len(labels)):
            empty = []
            values.append(empty)
        dictionary = dict(zip(labels, values))
        for ent in sentence.ents:
            dictionary[ent.label_].append(ent.text)
        
        return dictionary
        
    def words(self, sentence):
        words = []
        sentence = self.nlp(sentence)
        for token in sentence:
            words.append(str(token))
        return words
        
    def parse(self, sentence):
        analysis = {}
        parents2children = {}
        labels = {}
        sentence = self.nlp(sentence)
        for token in sentence:
            print(token.text, token.dep_, token.head.text, token.head.pos_,
                    [child for child in token.children])
            print('\n')
            parents2children[str(token)] = [child for child in token.children]
            analysis[token.dep_] = token.text
            
        return analysis, parents2children

    def shareWords(self, sentence1, sentence2):
        list1 = sentence1
        list2 = sentence2
        for e1 in list1:
            if e1 in list2:
                return True
        return False

    def commonWords(self, sentence1, sentence2):
        list1 = sentence1
        list2 = sentence2
        commonWords = list()
        for e1 in list1:
            if e1 in list2:
                commonWords.append(e1)
        return set(commonWords)

    def makePairs(self, inputList):
        outputList = ['']
        for elem in inputList:
            outputList[-1] += ' ' + elem
            outputList.append(elem)
        outputList.pop(-1)
        outputList.pop(0)
        return outputList

    def extractNumbers(self, sentence):
        numbers = list()
        for word in self.words(sentence):
            if word.isnumeric():
                numbers.append(int(word))
            else:
                try:
                    candNumber = w2n.word_to_num(word)
                    numbers.append(int(candNumber))
                except:
                    pass
        #for bathrooms
        candidates = ['a bathroom', 'another one', 'another bathroom']
        for pair in self.makePairs(self.words(sentence)):
            if self.shareWords(word, candidates):
                numbers.append(1)
        return numbers

        
    
if __name__ == '__main__':
    print("Write: ")
    sentence = input()
    p = Parser()
    p.parse(sentence)
    #print(p.parse(sentence))
    print(p.entities(sentence))
    squareMeters = None
    for word in p.words(sentence):
        if word.isnumeric():
            squareMeters = int(word)
            break
    print(squareMeters)
    print(p.makePairs(['ciao', 'come']))
    #print(p.noun_chunks(sentence))
    print(None == False)
    
    