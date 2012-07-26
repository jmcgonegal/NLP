import math
class LaplaceBigramLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    # TODO your code here
    
    self.bigrams = {}
    self.train(corpus)
    
  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    # TODO your code here
    for sentence in corpus.corpus: # iterate over sentences in the corpus
      for i in range(len(sentence.data)-1): # iterate over datums in the sentence
          hash = sentence.data[i].word , sentence.data[i+1].word
          if hash not in self.bigrams:
            self.bigrams[hash] = 0
          self.bigrams[hash] += 1

  
  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    total = len(self.bigrams) + len(sentence) - 1
    score = 0.0
    for i in range(len(sentence)-1):
      hash = sentence[i] , sentence[i+1]
      count = 1.
      if hash in self.bigrams:
        count += self.bigrams[hash]
      #score += math.log(count / total) 
      score += math.log(count)
      score -= math.log(total)
    return score
  