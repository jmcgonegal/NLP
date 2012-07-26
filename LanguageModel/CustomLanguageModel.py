import math
import collections
class CustomLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    # TODO your code here
    
    self.unigrams = collections.defaultdict(lambda: 0)
    self.bigrams = collections.defaultdict(lambda: 0)
    self.trigrams = collections.defaultdict(lambda: 0)
    self.continuation = collections.defaultdict(lambda: 0)
    self.counts = collections.defaultdict(lambda: 0)
    self.train(corpus)
  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    # TODO your code here
    for sentence in corpus.corpus: # iterate over sentences in the corpus
      for i in range(len(sentence.data)): # iterate over datums in the sentence
        hash = sentence.data[i].word
        self.unigrams[hash] += 1
      for i in range(len(sentence.data)-1): # iterate over datums in the sentence
        word1 = sentence.data[i].word
        word2 = sentence.data[i+1].word
        hash2 = word1 , word2
        if self.bigrams[hash2] == 0:
          
          # how many unique continuations does the word create
          # or how many ways does word1 appear before word2
          self.continuation[word1] += 1
        self.bigrams[hash2] += 1
      for i in range(len(sentence.data)-2): # iterate over datums in the sentence
        hash3 = sentence.data[i].word, sentence.data[i+1].word, sentence.data[i+2].word
        self.trigrams[hash3] += 1
    
    # 10 words occur 1 time, 5 words occur 2 times, etc
    for word in self.unigrams:
      self.counts[word] += 1
      


  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    score = 0.0
    discount = 0.75
    
    for i in range(1,len(sentence)-1):
      kn = 0.
      word = sentence[i]
      last_word = sentence[i-1]
      count_last_word = self.unigrams[last_word]
      bigram = last_word, word

      p_continue = self.continuation[word] / float(len(self.bigrams))
      p_continue += 0.01
      
        
      max = float(self.bigrams[bigram] - discount)

      if max < 0:
        max = 0.

      types_discounted = self.continuation[last_word] #cont_count
      if count_last_word > 0:
        lamda = discount / count_last_word * types_discounted
        kn += max / float(self.unigrams[last_word])
      else:
        lamda = discount * 0.1
        
      weighted_continuation = lamda * p_continue

      kn += weighted_continuation
        #print kn
      #else:
        #print last_word
      if kn > 0:
        score += math.log(kn)
      #score += math.log(self.continuation[sentence[i]])
      #score -= math.log(len(self.bigrams))
      

    return score
