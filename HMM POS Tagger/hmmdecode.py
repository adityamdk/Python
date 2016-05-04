
import sys
import math

import csv

#Structure Definitions
###############################################################################################################################
# This structure stores the transition probability between tags 
TransitionProbablity = {}
# This structure stores the Emission probability between tags and words  
EmissionProbablity = {}
tag_set = set()
###############################################################################################################################


#functions:
###############################################################################################################################

#Processes the input file and generates the Part of speech tags
def process_file(input):
    file = open(input, 'r')
    OutPutFile = open('hmmoutput.txt', 'w')

	
    for line in file:
        line = line.strip()
        #since using LOg 1 we are using 0 here 
        EachStateProbablity = {'q0': 0.0}
        StateSource = []
        WordOfLine = line.split()
        for word in WordOfLine:
            TokenProbablity = ComputeProbablity(word, EachStateProbablity, StateSource)
            EachStateProbablity = TokenProbablity
        ListOfTags = []
        MaxValue, BestTag = -1*sys.maxint, None
        for key, value in EachStateProbablity.iteritems():
            if value > MaxValue:
                MaxValue = value
                BestTag = key
        ListOfTags.append(BestTag)
        PrevTag = BestTag
        for index in xrange(len(StateSource)-1, 0, -1):
            tag = StateSource[index][PrevTag]
            ListOfTags.append(tag)
            PrevTag = tag
        ListOfTags.reverse()
        out_tokens = []
        for index, word in enumerate(WordOfLine):
            out_tokens.append('%s/%s' % (word, ListOfTags[index]))
        Output = ' '.join(out_tokens)
        OutPutFile.write('%s\n' % Output)

    OutPutFile.close()
	
	

#This function generates a dictionary of tags and associated probabilities for each word
	
def ComputeProbablity(word, EachStateProbablity, StateSource):

    global EmissionProbablity, TransitionProbablity
    PossibleWordTags = {}
    overlapFlag = False
	
	
	
    if word not in EmissionProbablity: # unknown word case
        for key in EachStateProbablity:
            for tag in TransitionProbablity[key]:
                if tag != 'others':
                    PossibleWordTags[tag] = 1.0  # set emission probabilities for all tags as 1
        overlapFlag = True
	
	
    else: 
        # word present in EmissionProbablity
        PossibleWordTags = EmissionProbablity[word]
        TagsofInput = set(PossibleWordTags.keys())
        # check if any transition is possible
        
        for key in EachStateProbablity:
            transitionTags = set(TransitionProbablity[key].keys())
            if set(transitionTags).intersection(TagsofInput):
                overlapFlag = True
                break

    # now the main calculation starts
    TagAndProbOfWord = {}  # contains each possible tag for the word with associated probabilities
    
	
	
    TagAndPrevTag = {}  # source of a given tag, that is which tag of previous state is source of current tag
    
	
    for PrevTag, PrevProb in EachStateProbablity.iteritems():
        for tag, EP in PossibleWordTags.iteritems():
            TPVALUE = 0.0

            if overlapFlag:
                if tag in TransitionProbablity[PrevTag]:
                    TPVALUE = TransitionProbablity[PrevTag][tag]
                else:
                    continue
            else:
                TPVALUE = TransitionProbablity[PrevTag]['others']
            FinalStateProb = PrevProb + EP + TPVALUE

            if tag not in TagAndProbOfWord or FinalStateProb > TagAndProbOfWord[tag]:
                TagAndProbOfWord[tag] = FinalStateProb
                TagAndPrevTag[tag] = PrevTag

    StateSource.append(TagAndPrevTag)
    return TagAndProbOfWord

###############################################################################################################################


input = sys.argv[1]

file = open('hmmmodel.txt', 'r')
FilePointer = csv.reader(file, delimiter=',')
BasicUnit = FilePointer.next()



while BasicUnit[0] != '<emission_end>':
    if BasicUnit[0] in EmissionProbablity:
        EmissionProbablity[BasicUnit[0]][BasicUnit[1]] = math.log(float(BasicUnit[2])) # handling floating point underflow case
    else:
        EmissionProbablity[BasicUnit[0]] = {BasicUnit[1]: math.log(float(BasicUnit[2]))}

    BasicUnit = FilePointer.next()
BasicUnit = FilePointer.next()
while BasicUnit:
    tag_set.add(BasicUnit[0])
    if BasicUnit[0] in TransitionProbablity:
        TransitionProbablity[BasicUnit[0]][BasicUnit[1]] = math.log(float(BasicUnit[2]))
    else:
        TransitionProbablity[BasicUnit[0]] = {BasicUnit[1]: math.log(float(BasicUnit[2]))}
    BasicUnit = next(FilePointer, None)




process_file(input)