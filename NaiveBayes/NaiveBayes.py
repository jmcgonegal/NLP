# NLP Programming Assignment #3
# NaiveBayes
# 2012

#
# The area for you to implement is marked with TODO!
# Generally, you should not need to touch things *not* marked TODO
#
# Remember that when you submit your code, it is not run from the command line 
# and your main() will *not* be run. To be safest, restrict your changes to
# addExample() and classify() and anything you further invoke from there.
#


import sys
import getopt
import os
import math
import collections
import re
class NaiveBayes:
  class TrainSplit:
    """Represents a set of training/testing data. self.train is a list of Examples, as is self.test. 
    """
    def __init__(self):
      self.train = []
      self.test = []

  class Example:
    """Represents a document with a label. klass is 'pos' or 'neg' by convention.
       words is a list of strings.
    """
    def __init__(self):
      self.klass = ''
      self.words = []


  def __init__(self):
    """NaiveBayes initialization"""
    self.FILTER_STOP_WORDS = False
    self.stopList = set(self.readFile('../data/english.stop'))
    self.numFolds = 10
    self.pos = collections.defaultdict(lambda: 0)
    self.pos_count = 0
    self.neg = collections.defaultdict(lambda: 0)
    self.neg_count = 0
    self.pos_class = 0
    self.neg_class = 0
    regex_string = r"""
    (?:[a-z][a-z'\-_]+[a-z])       # Words with apostrophes or dashes.
    |
    (?:[+\-]?\d+[,/.:-]\d+[+\-]?)  # Numbers, including fractions, decimals.
    |
    (?:[\w_]+)                     # Words without apostrophes or dashes.
    |
    (?:\.(?:\s*\.){1,})            # Ellipsis dots. 
    |
    (?:\S)                         # Everything else that isn't whitespace.
    """
    self.re_comp = re.compile(regex_string, re.VERBOSE )

  #############################################################################
  # TODO TODO TODO TODO TODO 
  def stem(self,word):
    leaves = "s", "es", "ed", "er", "ly", "ing"
    for leaf in leaves:
      if word[-len(leaf):] == leaf:
        return word[:-len(leaf)]
      
  def get_words(self, words):
    #return words
    count_once = collections.defaultdict(lambda: False)
    for word in words:
      #if word == '"' or word == ":" or word == "(" or word == ")" or word == "." or word == "_" or word == ",":
      #  pass
      #else:
      count_once[word] = True
      
    parsed_words = []
    for word in words:
      #if word == '"' or word == ":" or word == "(" or word == ")" or word == "." or word == "_":
      #  pass
      #else:
      if count_once[word]:
        count_once[word] = False
        parsed_words.append(word)
    return parsed_words
  
    '''parsed_words = []
    for word in words:
      new_words = word.split('_')
      for new_word in new_words:
        #new_word = self.removePostfix(new_word)
        parsed_words.append(new_word)'''
    #parsed_words = []
    '''for word in words:
      new_words = self.re_comp.findall(word)
      for new_word in new_words:
        #if re.search("[a-z]", new_word):
        new_word = self.stem(new_word)
        if new_word is not None:
          #new_word = new_word.replace("'","")
          parsed_words.append(new_word)'''
          
    #return parsed_words
  
  def classify(self, words):
    """ TODO
      'words' is a list of words to classify. Return 'pos' or 'neg' classification.
    """
    total = self.pos_class + self.neg_class
    pos = 0
    neg = 0
    
    
    #if self.pos_class > 0:
    pos += math.log(self.pos_class) 
    #if self.neg_class > 0:
    neg += math.log(self.neg_class)
    pos -= math.log(total)
    neg -= math.log(total)

    smooth = 1.0
    #print words
    
    
    
    parsed_words = self.get_words(words)

        
    for word in parsed_words:
      count_unique_occur = self.pos[word] + self.neg[word]
      
      count_word = self.pos[word]
      count_total_word = self.pos_count
      
      num = count_word + smooth
      dem = count_total_word + (len(self.pos) * smooth) 

      pos += math.log(num)
      pos -= math.log(dem)
      
      #count_unique_occur = self.neg[word]
      count_word = self.neg[word]
      count_total_word = self.neg_count
      num = count_word + smooth
      dem = count_total_word + (len(self.neg) * smooth)#count_unique_occur * smooth)

      neg += math.log(num)
      neg -= math.log(dem)

    #print self.pos_count, self.neg_count
    #print p_pos, p_neg #, class_p, class_n, class_p+class_n
    #print pos, neg, pos-neg
    if pos > neg:
      return 'pos'
    elif neg > pos:
      return 'neg'

  
  def addClassification(self, klass, words):
    if klass == 'pos':
      self.pos_class += 1
    elif klass == 'neg':
      self.neg_class += 1
    
    parsed_words = self.get_words(words)
    
    for word in parsed_words:
      if klass == 'pos':
        #if word not in self.pos:
        #  self.pos[word] = 0
        self.pos[word] += 1
        self.pos_count += 1
      elif klass == 'neg':
        #if word not in self.neg:
        #  self.neg[word] = 0
        self.neg[word] += 1
        self.neg_count += 1
        
  def addExample(self, klass, words):
    """
     * TODO
     * Train your model on an example document with label klass ('pos' or 'neg') and
     * words, a list of strings.
     * You should store whatever data structures you use for your classifier 
     * in the NaiveBayes class.
     * Returns nothing
    """

    self.addClassification(klass,words)

    
  # TODO TODO TODO TODO TODO 
  #############################################################################
  
  
  def readFile(self, fileName):
    """
     * Code for reading a file.  you probably don't want to modify anything here, 
     * unless you don't like the way we segment files.
    """
    contents = []
    f = open(fileName)
    for line in f:
      contents.append(line)
    f.close()
    result = self.segmentWords('\n'.join(contents)) 
    return result

  
  def segmentWords(self, s):
    """
     * Splits lines on whitespace for file reading
    """
    return s.split()

  
  def trainSplit(self, trainDir):
    """Takes in a trainDir, returns one TrainSplit with train set."""
    split = self.TrainSplit()
    posTrainFileNames = os.listdir('%s/pos/' % trainDir)
    negTrainFileNames = os.listdir('%s/neg/' % trainDir)
    for fileName in posTrainFileNames:
      example = self.Example()
      example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
      example.klass = 'pos'
      split.train.append(example)
    for fileName in negTrainFileNames:
      example = self.Example()
      example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
      example.klass = 'neg'
      split.train.append(example)
    return split

  def train(self, split):
    for example in split.train:
      words = example.words
      if self.FILTER_STOP_WORDS:
        words =  self.filterStopWords(words)
      self.addExample(example.klass, words)

  def crossValidationSplits(self, trainDir):
    """Returns a lsit of TrainSplits corresponding to the cross validation splits."""
    splits = [] 
    posTrainFileNames = os.listdir('%s/pos/' % trainDir)
    negTrainFileNames = os.listdir('%s/neg/' % trainDir)
    #for fileName in trainFileNames:
    for fold in range(0, self.numFolds):
      split = self.TrainSplit()
      for fileName in posTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
        example.klass = 'pos'
        if fileName[2] == str(fold):
          split.test.append(example)
        else:
          split.train.append(example)
      for fileName in negTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
        example.klass = 'neg'
        if fileName[2] == str(fold):
          split.test.append(example)
        else:
          split.train.append(example)
      splits.append(split)
    return splits


  def test(self, split):
    """Returns a list of labels for split.test."""
    labels = []
    for example in split.test:
      words = example.words
      if self.FILTER_STOP_WORDS:
        words =  self.filterStopWords(words)
      guess = self.classify(words)
      labels.append(guess)
    return labels
  
  def buildSplits(self, args):
    """Builds the splits for training/testing"""
    trainData = [] 
    testData = []
    splits = []
    trainDir = args[0]
    if len(args) == 1: 
      print '[INFO]\tPerforming %d-fold cross-validation on data set:\t%s' % (self.numFolds, trainDir)

      posTrainFileNames = os.listdir('%s/pos/' % trainDir)
      negTrainFileNames = os.listdir('%s/neg/' % trainDir)
      for fold in range(0, self.numFolds):
        split = self.TrainSplit()
        for fileName in posTrainFileNames:
          example = self.Example()
          example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
          example.klass = 'pos'
          if fileName[2] == str(fold):
            split.test.append(example)
          else:
            split.train.append(example)
        for fileName in negTrainFileNames:
          example = self.Example()
          example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
          example.klass = 'neg'
          if fileName[2] == str(fold):
            split.test.append(example)
          else:
            split.train.append(example)
        splits.append(split)
    elif len(args) == 2:
      split = self.TrainSplit()
      testDir = args[1]
      print '[INFO]\tTraining on data set:\t%s testing on data set:\t%s' % (trainDir, testDir)
      posTrainFileNames = os.listdir('%s/pos/' % trainDir)
      negTrainFileNames = os.listdir('%s/neg/' % trainDir)
      for fileName in posTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
        example.klass = 'pos'
        split.train.append(example)
      for fileName in negTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
        example.klass = 'neg'
        split.train.append(example)

      posTestFileNames = os.listdir('%s/pos/' % testDir)
      negTestFileNames = os.listdir('%s/neg/' % testDir)
      for fileName in posTestFileNames:
        example = self.Example()
        example.words = self.readFile('%s/pos/%s' % (testDir, fileName)) 
        example.klass = 'pos'
        split.test.append(example)
      for fileName in negTestFileNames:
        example = self.Example()
        example.words = self.readFile('%s/neg/%s' % (testDir, fileName)) 
        example.klass = 'neg'
        split.test.append(example)
      splits.append(split)
    return splits
  
  def filterStopWords(self, words):
    """Filters stop words."""
    filtered = []
    for word in words:
      if not word in self.stopList and word.strip() != '':
        filtered.append(word)
    return filtered



def main():
  nb = NaiveBayes()
  #sys.argv = ['','-f', '../data/imdb1']
  #sys.argv = ['', '../data/imdb1']
  (options, args) = getopt.getopt(sys.argv[1:], 'f')
  if ('-f','') in options:
    nb.FILTER_STOP_WORDS = True

  splits = nb.buildSplits(args)
  avgAccuracy = 0.0
  fold = 0
  for split in splits:
    classifier = NaiveBayes()
    accuracy = 0.0
    for example in split.train:
      words = example.words
      if nb.FILTER_STOP_WORDS:
        words =  classifier.filterStopWords(words)
      classifier.addExample(example.klass, words)
  
    for example in split.test:
      words = example.words
      if nb.FILTER_STOP_WORDS:
        words =  classifier.filterStopWords(words)
      guess = classifier.classify(words)
      if example.klass == guess:
        accuracy += 1.0
      #else:
        #print guess, example.words
    accuracy = accuracy / len(split.test)
    avgAccuracy += accuracy
    print '[INFO]\tFold %d Accuracy: %f' % (fold, accuracy) 
    fold += 1
  avgAccuracy = avgAccuracy / fold
  print '[INFO]\tAccuracy: %f' % avgAccuracy

if __name__ == "__main__":
    # no stop words
    sys.argv = ['','-f', '../data/imdb1']
    main()
    # with all words
    sys.argv = ['', '../data/imdb1']
    main()
