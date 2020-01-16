from parser import Parser


class Summarizer:
    def __init__(self):
        self.parser = Parser()

    def summarize(self, text):
        sentences = self.parser.splitSentences(text)
        #print(sentences)
        (keywords, wordCount) = self.parser.getKeywords(text)
        topKeywords = self.getTopKeywords(keywords[:10], wordCount)

        tagged = self.parser.getTagsForWords(text)
        print(tagged)
        NP = self.parser.getNounPositions('NP', tagged, text)
        print(NP)
        PRP = self.parser.getProNounPositions(tagged, text)
        print(PRP)
        text = self.parser.pronounReplaceWithNearNoun(text, PRP, NP)
        sentences = self.parser.splitSentences(text)
        print(sentences)

        result = self.computeScore(sentences, topKeywords)
        result = self.sortScore(result)

        return result

    def getTopKeywords(self, keywords, wordCount):
        # Add getting top keywords in the database here
        for keyword in keywords:
            articleScore = 1.0 * keyword['count'] / wordCount
            keyword['totalScore'] = articleScore * 1.5

        return keywords

    def sortScore(self, dictList):
        return sorted(dictList, key=lambda x: -x['totalScore'])

    def sortSentences(self, dictList):

        return sorted(dictList, key=lambda x: x['order'])

    def computeScore(self, sentences, topKeywords):
        keywordList = [keyword['word'] for keyword in topKeywords]
        summaries = []

        for i, sentence in enumerate(sentences):
            sent = self.parser.removePunctations(sentence)
            words = self.parser.splitWords(sent)

            sbsFeature = self.sbs(words, keywordList)
            dbsFeature = self.dbs(words, topKeywords, keywordList)

            sentenceLength = self.parser.getSentenceLengthScore(words)
            sentencePosition = self.parser.getSentencePositionScore(i, len(sentences))
            keywordFrequency = (sbsFeature + dbsFeature) / 2.0 * 10.0
            totalScore = (0.5 + keywordFrequency * 2.0 + sentenceLength * 0.5 + sentencePosition * 1.0) / 4.0

            summaries.append({
                'totalScore': totalScore,
                'sentence': sentence,
                'order': i
            })

        return summaries

    def sbs(self, words, keywordList):
        score = 0.0
        if len(words) == 0:
            return 0
        for word in keywordList:
            if word in words:
                score += 1
        return score / len(keywordList)

    def dbs(self, words, topKeywords, keywordList):
        k = len(list(set(words) & set(keywordList))) + 1
        summ = 0.0
        firstWord = {}
        secondWord = {}

        for i, word in enumerate(words):
            if word in keywordList:
                index = keywordList.index(word)

                if firstWord == {}:
                    firstWord = {'i': i, 'score': topKeywords[index]['totalScore']}
                else:
                    secondWord = firstWord
                    firstWord = {'i': i, 'score': topKeywords[index]['totalScore']}
                    distance = firstWord['i'] - secondWord['i']

                    summ += (firstWord['score'] * secondWord['score']) / (distance ** 2)

        return (1.0 / k * (k + 1.0)) * summ