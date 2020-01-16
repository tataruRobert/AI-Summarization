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
