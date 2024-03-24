#  A text generating algorithm using Markov Chains. The program calculates the   
#  probability for every word in the text to follow the previous word, and randomly 
#  chooses the next word with those probabilities as weights.
#  
#  Uses Martin Majlis's wikipedia api wrapper for python, and Francisco Rodrigues's unofficial ao3 api. If you want to use a different text simply fork the repl.it, add a file containing the text, and change one of the current 'existing texts' to the name and address of the new file.
#Two known bugs: sometimes deletes the last letter of a word that is followed by punctuation, also somtimes deletes spaces between words.
import random
import wikipediaapi
import AO3
wiki_wiki = wikipediaapi.Wikipedia('en')
global wiki_page, wordsFile, wordsList, ao3Work

#Gets the words in the file, returns as list. Punctuation marks are their own words, spaces are removed.
def getWordsInFile(file):
  wordsList = []
  for word in file:
    wordWithoutPunct = ""
    for letter in word:
      if(letter.isalpha() or letter.isnumeric() or letter == "'"):
        wordWithoutPunct += letter
      else:
        if(len(wordWithoutPunct) > 0):
          wordsList.append(wordWithoutPunct)
        if(letter != " "):
          wordsList.append(letter)
        wordWithoutPunct = ""
  return wordsList

#gets the words from a wiki_page.text string, same as get words in file
def getWordsInWiki(wiki):
  wordsList = []
  wordWithoutPunct = ""
  for letter in wiki:
    if(letter.isalpha() or letter.isnumeric() or letter == "'"):
      wordWithoutPunct += letter
    else:
      if(len(wordWithoutPunct) > 0):
        wordsList.append(wordWithoutPunct)
      if(letter != " "):
        wordsList.append(letter)
      wordWithoutPunct = ""
  return wordsList

#gets the words from an ao3Work object
def getWordsInFic(ao3Work):
  wordsList = []
  totalText = ""
  for i in range(ao3Work.nchapters):
    totalText += ao3Work.chapters[i].title + "\n" + ao3Work.chapters[i].text
  #For loop gets the entire text of the work
  wordWithoutPunct = ""
  for letter in totalText:
    if(letter.isalpha() or letter.isnumeric() or letter == "'"):
      wordWithoutPunct += letter
    else:
      if(len(wordWithoutPunct) > 0):
        wordsList.append(wordWithoutPunct)
      if(letter != " "):
        wordsList.append(letter)
      wordWithoutPunct = ""
  return wordsList

#gets the probability of all words in the text to follow the given word
def getSingleWordProbability(word, orderedWordList):
  probabilityList = {}
  numOfTotalOccurances = 0.0
  for eachWord in orderedWordList:
    probabilityList[eachWord] = 0.0;
  for i in range(len(orderedWordList)):
    if(orderedWordList[i-1] == word):
      probabilityList[orderedWordList[i]] += 1.0
      numOfTotalOccurances += 1.0
  for key in probabilityList:
    probabilityList[key] /= numOfTotalOccurances
  return probabilityList

#gets all the probability dictionaries for all of the words, returns as a dictionary of dictionaries
def getAllWordProbabilities(orderedWordList):
  listOfProbs = {}
  listOfAlreadySeenWords = []
  for word in orderedWordList:
    if(not (word in listOfAlreadySeenWords)):
      listOfProbs[word] = getSingleWordProbability(word, orderedWordList)
      listOfAlreadySeenWords.append(word)
  return listOfProbs

#Uses the probabilities as weights when choosing the next word by getting a random number 0 to 1; if the number is less than the probability of the word choose that word, otherwise subtract the probability of the word from the number generated.
def chooseNextWord(prevWord, probDictDict):
  nextWordProbs = probDictDict[prevWord]
  randomChoice = random.random()
  for word in nextWordProbs:
    if(randomChoice <= nextWordProbs[word]):
      return word
    randomChoice -= nextWordProbs[word]
  return "\tThis shouldn't have happened. Whoopsie\t"

#Starts the text by treating it as the beginning of a sentance, this won't work if there is no periods in the text.
def chooseFirstWord(probDictDict):
  return chooseNextWord(".", probDictDict)

#Runs the menu that the user interacts with. There is no error trapping, so bad input will simply break the program.
def userInterface():
  global wordsList, wordsFile, wiki_page, ao3Work
  print("1. Use Wikipedia Article\n2. Use AO3 text\n3. Use an existing text")
  uChoice = int(input())
  if(uChoice == 1):
    while(True):
      print("Enter the title of a Wikipedia page:")
      wikiName = input()
      wiki_page = wiki_wiki.page(wikiName)
      if(wiki_page.exists()):
        break
      else:
        print("Failed to get text")
    wordsFile = wiki_page.text
    wordsList = getWordsInWiki(wordsFile)
  elif(uChoice == 2):
    print("Enter the url or work ID of the text")
    textAddress = input()
    if("https" in textAddress):
      textAddress = AO3.utils.workid_from_url(textAddress)
    ao3Work = AO3.Work(textAddress)
    wordsList = getWordsInFic(ao3Work)
  else:
    print("1. Alice in Wonderland Ch.1\n2. The Bee Movie\n3. The Book of Genesis")
    uChoice = int(input())
    if(uChoice == 1):
      wordsFile = open("alice_in_wonderland.txt")
    elif(uChoice == 2):
      wordsFile = open("bee_movie.txt")
    elif(uChoice == 3):
      wordsFile = open("genesis.txt")
    else:
      wordsFile = open("test.txt")
    wordsList = getWordsInFile(wordsFile)
  beginCreating()

#Creates the new text using the markov chain for as long as the user inputs.
def beginCreating():
  global wiki_page, wordsFile, wordsList
  probList = getAllWordProbabilities(wordsList)

  print("Create:\n1. Set number of tokens (1 token is 1 word or 1 punctuation mark, spaces are 0 tokens)\n2. Set number of paragraphs (One paragraph is until a line break is generated, length will vary based on input text)")
  uChoice = int(input())
  if(uChoice == 1):
    print("Enter number of tokens to generate:")
    uChoice = int(input())
    previousWord = chooseFirstWord(probList)
    print(previousWord + " ", end='')
    spaceOrNot = ""
    for i in range(uChoice):
      previousWord = chooseNextWord(previousWord, probList)
      if(not (previousWord.isalpha() or previousWord.isnumeric() or "'" in previousWord or previousWord == " ")): 
        print("\b", end='')
      if(previousWord == "(" or previousWord == "{" or previousWord == "["): spaceOrNot = ""
      else: spaceOrNot = " "
      print(previousWord + spaceOrNot, end='')
  else:
    print("Enter number of paragraphs:")
    uChoice = int(input())
    counter = 0
    previousWord = chooseFirstWord(probList)
    print(previousWord + " ", end='')
    spaceOrNot = ""
    while(uChoice > counter):
      previousWord = chooseNextWord(previousWord, probList)
      if(previousWord == "\n"):
        counter += 1
      if(not (previousWord.isalpha() or previousWord.isnumeric() or "'" in previousWord or previousWord == " ")): 
        print("\b", end='')
      if(previousWord == "(" or previousWord == "{" or previousWord == "["): spaceOrNot = ""
      else: spaceOrNot = " "
      print(previousWord + spaceOrNot, end='')

#Main: Prints some warnings then runs the program.
print("Some parts of the program may run slowly, especially when inputting larger texts.")
print("Will not work if given texts with no periods (.) in them.")
userInterface()
