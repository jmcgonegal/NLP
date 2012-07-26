import math
import collections
class StupidBackoffLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    # TODO your code here
    self.unigrams = collections.defaultdict(lambda: 0)
    self.bigrams = collections.defaultdict(lambda: 0)
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    # TODO your code here
    for sentence in corpus.corpus: # iterate over sentences in the corpus
      # unigrams
      for i in range(len(sentence.data)): # iterate over datums in the sentence
          hash = sentence.data[i].word

          self.unigrams[hash] += 1
      # bigrams
      for i in range(1,len(sentence.data)): # iterate over datums in the sentence
          hash2 = sentence.data[i-1].word , sentence.data[i].word

          self.bigrams[hash2] += 1

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # count of words / count of prefix
    # TODO your code here
    score = 0.0
    for i in range(len(sentence)-1):
      
      word1 = sentence[i]
      word2 = sentence[i-1]
      bihash = word1 , word2
      #if hash in self.unigrams:
      if self.unigrams[word1] > 0:
        #score += math.log(self.unigrams[wi] + self.unigrams[wn1])
        score += math.log(self.unigrams[word1])
        if self.unigrams[word2] > 0:
          score -= math.log(self.unigrams[word2])
      #if self.bigrams[bihash] > 0:
      #  score += math.log(self.bigrams[bihash])
      #  score -= math.log(len(self.bigrams))
      else:

        total = len(sentence) + len(self.unigrams)
        count = 1.
        if word1 in self.unigrams:
          count += self.unigrams[word1]
          
        score += math.log(0.4 * count)
        score -= math.log(total)

    return score
