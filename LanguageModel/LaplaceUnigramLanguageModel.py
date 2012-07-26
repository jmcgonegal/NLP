import math, collections

class LaplaceUnigramLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    # TODO your code here
    self.wordcount = {}
    self.mycount = 0
    
    self.train(corpus)
    

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    # TODO your code here

    for sentence in corpus.corpus: # iterate over sentences in the corpus
      for datum in sentence.data: # iterate over datums in the sentence

        if datum.word not in self.wordcount:
          self.wordcount[datum.word] = 0
        self.wordcount[datum.word] += 1
        self.mycount += 1

    

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    score = 0.0


    total = len(sentence) + len(self.wordcount)
    for word in sentence:
      count = 0.
      if word in self.wordcount:
        count += self.wordcount[word]
      count += 1
      total_plus_one = total#self.mycount + len(sentence)
      #probability = math.log(count / total_plus_one)
      #score += probability
      score += math.log(count)
      score -= math.log(total_plus_one)
    # NOTE: a simpler method would be just score = sentence.size() * - Math.log(words.size()).
    # we show the 'for' loop for insructive purposes.
    return score

