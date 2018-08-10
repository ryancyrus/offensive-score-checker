import re

def showPrompt():
    '''
    Returns respone and file range selected by user for running the script else returns False.
    Default: Process all 15 input files.
    '''
    print("Offenscore Calculator\n".upper())
    print("This script will process the files included for the challenge to calculate score.\n")
    response = input("Press Y then Enter to proceed or any key then Enter to quit.\n")
    if response == 'y' or response == 'Y':
        startFile = 1
        endFile = 15
        return response, startFile, endFile
    print("QUITTING...!")
    return False, False, False

def findSpecialChars(wordList):
    '''
    Find the speacial characters from the keywords which
    should not be cleaned from the sentences.
    '''
    leftWords = re.sub(r'[a-z ]+', '', "".join(wordList))
    return "".join(set(leftWords))

def readKeywordsList(filename):
    '''
    Reads the keywords from the file and returns them as list.
    '''
    try:
        with open(filename, 'r') as f:
            return f.read().strip().lower().split("\n")
    except FileNotFoundError:
        print("{} was not found.".format(filename))
        return []   

def readKeywordsDict(filename):
    '''
    Reads the keywords from the file and
    returns them as Dictionary with first word as key.
    '''
    try:
        with open(filename, 'r') as f:
            return {j.split(" ")[0]: j for j in f.read().strip().lower().split("\n") }
    except FileNotFoundError:
        print("{} was not found.".format(filename))
        return {}

def readInputFiles(filename):
    '''
    Returns the data read from the file read.
    '''
    try:
        with open(filename, 'r') as f:
            return f.read().strip().lower()
    except FileNotFoundError:
        print("{} was not found.".format(filename))
        return ""

def writeOutput(data, fileToWrite):
    '''
    Writes the score outputs to the file.
    '''
    try:
        with open(fileToWrite, 'w') as f:
            f.write("\n".join(["{}:{}".format(key, score) for key, score in data.items()]))
        return True
    except IOError:
        print("Oops, something went wrong.");
        return False

# def cleanNormalScore(data, lowRiskList, highRiskList, charactersToKeep):
#     '''
#     Smart Mode:
#     Leading and Trailing characters around the offensive keyword are ignored.
#     Example: kkkittenn will still be detected as kitten.

#     Cleans the data by removing the speacial characters and punctuations
#     except the ones already in keywords.
    
#     Returns the cleaned string.
#     '''
#     words = re.compile('[^a-z{} ]'.format(charactersToKeep))
#     sentence = re.sub(words, "", data)

#     low_score = (sum(sentence.count(low_word) for low_word in lowRiskList))
#     high_score = (sum(sentence.count(high_word) for high_word in highRiskList))
#     return low_score + (high_score * 2)

# def cleanStrictScoreRegex(data, lowRiskList, highRiskList, charactersToKeep):
#     '''
#     Strict Mode using Regex:
#     Scores only when the exact keyword is matched.

#     Cleans the data by removing the speacial characters and punctuations
#     except the ones already in keywords.
    
#     Returns the cleaned string.
#     '''
#     words = re.compile('[^a-z{} ]'.format(charactersToKeep))
#     sentence = re.sub(words, "", data)

#     low_score = 0
#     high_score = 0
#     for low_word in lowRiskList:
#         pattern = re.compile(r'\b' + re.escape(low_word) + r'\b')
#         matches = re.findall(pattern, sentence)
#         low_score += len(matches)

#     for high_word in highRiskList:
#         pattern = re.compile(r'\b' + re.escape(high_word) + r'\b')
#         matches = re.findall(pattern, sentence)
#         high_score += len(matches)
#     print("Regex Method:", low_score + (high_score * 2))
#     return low_score + (high_score * 2)

def cleanStrictScoreDict(data, lowRiskDict, highRiskDict, charactersToKeep):
    '''
    Strict Mode using Dictionary Lookup(Faster than Regex):
    Scores only when the exact keyword is matched.

    Cleans the data by removing the speacial characters and punctuations
    except the ones already in keywords.
    
    Returns the cleaned string.
    '''
    
    words = re.compile('[^a-z{} ]'.format(charactersToKeep))
    sentence = re.sub(words, "", data).split(" ")
    lowScore = 0
    highScore = 0
    for word in range(len(sentence)):
        wordToMatch = sentence[word]
        
        lowHit = lowRiskDict.get(wordToMatch)
        if lowHit != None and (len(lowHit) > len(wordToMatch)):
            wordsOfPhrase = lowHit.split(" ")
            phraseHit = True
            for w in range(len(wordsOfPhrase)):
                if sentence[w + word] != wordsOfPhrase[w]:
                    phraseHit = False
                    break
            if phraseHit:
                lowScore += 1
        elif lowHit != None:
            lowScore += 1
        
        highHit = highRiskDict.get(wordToMatch)
        if highHit != None and (len(highHit) > len(wordToMatch)):
            wordsOfPhrase = highHit.split(" ")
            phraseHit = True
            for w in range(len(wordsOfPhrase)):
                if sentence[w + word] != wordsOfPhrase[w]:
                    phraseHit = False
                    break
            if phraseHit:
                highScore += 1
        elif highHit != None:
            highScore += 1

    return(lowScore + (highScore * 2))


def processFiles(lowRiskPhrasesFile, HighRiskPhrasesFile, inputFileList):
    '''
    Process all files and calculate the score for each one of them
    Returns the output dictionary.
    '''
    # Read the phrases as Dictionary
    lowrisk = readKeywordsDict(lowRiskPhrasesFile)
    highrisk = readKeywordsDict(HighRiskPhrasesFile)
    charactersToKeep = findSpecialChars(lowrisk.values()) + findSpecialChars(highrisk.values())
    # Read the input files and
    # Generate the scores 
    output = {}
    for i in inputFileList:
        data = readInputFiles(i)
        if data:
            output[i] = cleanStrictScoreDict(data, lowrisk, highrisk, charactersToKeep)
    return output


if __name__ == "__main__":
    response, startF, endF = showPrompt()
    if response:
        filesToRead = ["input{:02}.txt".format(i) for i in range(int(startF), int(endF) + 1)]
        lowRiskFile = "low_risk_phrases.txt"
        highRiskFile = "high_risk_phrases.txt"
        output = processFiles(lowRiskFile, highRiskFile, filesToRead)
        fileToWrite = "output.txt"
        if output and writeOutput(output, fileToWrite):
            print("Scores added to the {} file.".format(fileToWrite))
        else:
            print("Nothing processed.")
