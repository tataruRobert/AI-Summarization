import re
from nltk import word_tokenize
from treetagger import TreeTagger
tt = TreeTagger(path_to_treetagger='/Users/Mihaela/Downloads/TreeTagger/')

class Parser:
    def __init__(self):
        self.ideal = 20.0
        self.stopWords = self.getStopWords()

    def getKeywords(self, text):
        text = self.removePunctations(text)
        words = self.splitWords(text)
        words = self.removeStopWords(words)
        uniqueWords = list(set(words))

        keywords = [{'word': word, 'count': words.count(word)} for word in uniqueWords]
        keywords = sorted(keywords, key=lambda x: -x['count'])

        return (keywords, len(words))

    def getSentenceLengthScore(self, sentence):
        return (self.ideal - abs(self.ideal - len(sentence))) / self.ideal

    def getSentencePositionScore(self, i, sentenceCount):
        normalized = i / (sentenceCount * 1.0)

        if normalized > 0 and normalized <= 0.1:
            return 0.17
        elif normalized > 0.1 and normalized <= 0.2:
            return 0.23
        elif normalized > 0.2 and normalized <= 0.3:
            return 0.14
        elif normalized > 0.3 and normalized <= 0.4:
            return 0.08
        elif normalized > 0.4 and normalized <= 0.5:
            return 0.05
        elif normalized > 0.5 and normalized <= 0.6:
            return 0.04
        elif normalized > 0.6 and normalized <= 0.7:
            return 0.06
        elif normalized > 0.7 and normalized <= 0.8:
            return 0.04
        elif normalized > 0.8 and normalized <= 0.9:
            return 0.04
        elif normalized > 0.9 and normalized <= 1.0:
            return 0.15
        else:
            return 0

    def getTagsForWords(self, textLn2):
        tokens = word_tokenize(textLn2)
        tagged = tt.tag(tokens)
        return tagged

    def splitSentences(self, text):
        text = text.strip()
        # print(len(text))
        text_tokens = re.split("\. |\? |\! ", text)
        return text_tokens

    def splitWords(self, sentence):
        return sentence.lower().split()

    def removePunctations(self, text):
        return ''.join(t for t in text if t.isalnum() or t == ' ')

    def removeStopWords(self, words):
        return [word for word in words if word not in self.stopWords]

    def getStopWords(self):
        with open('stopWords.txt') as file:
            words = file.readlines()

        return [word.replace('\n', '') for word in words]

    def getNounPositions(self, type, tagged, lineIn):
        nounPosi = {}
        for item in tagged:
            if str(item[1]).startswith(type):
                nounPosi[item[0]] = -1
        for key in nounPosi.keys():
            regExpression = r'\b' + key.lower() + r'\b'
            nounsi = [m.start() for m in re.finditer(regExpression, lineIn.lower())]
            nounPosi[key] = nounsi
        return nounPosi

    def pronounReplaceWithNearNoun(self, lineIn, PRP, NNP):
        replacePRP = []
        for key in PRP.keys():
            for pos in PRP[key]:
                print('---------', key, '------', pos, '-----')
                nearNoun = self.getNearestPreviousNoun(NNP, pos, lineIn)
                replacePRP.append((key, pos, nearNoun))

        replacePRP = sorted(replacePRP, key=lambda x: (-x[1], x[0], x[2]))

        lineInReplacePronn = lineIn
        for prpRep in replacePRP:
            lineInReplacePronn = lineInReplacePronn[:prpRep[1]] + prpRep[2] + lineInReplacePronn[
                                                                              prpRep[1] + len(prpRep[0]):]
        return lineInReplacePronn

    def getNearestPreviousNoun(self, NNP, posiOfPronoun, lineIn):
        minimumDiff = len(lineIn)
        nearKey = ''
        for keyNNP in NNP.keys():
            for posNoun in NNP[keyNNP]:
                if (posiOfPronoun > posNoun):
                    if (minimumDiff > (posiOfPronoun - posNoun)):
                        minimumDiff = posiOfPronoun - posNoun
                        nearKey = keyNNP
        return nearKey

    def getProNounPositions(self, tagged, lineIn):
        proNounPosi = {}
        for item in tagged:
            if str(item[1]).startswith("P"):
                proNounPosi[item[0].lower()] = -1

        for key in proNounPosi.keys():
            regExpression = r'\b' + key.lower() + r'\b'
            pronounsi = [m.start() for m in re.finditer(regExpression, lineIn.lower())]
            proNounPosi[key] = pronounsi
        return proNounPosi