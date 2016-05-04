import sys
#Structure Definitions
###############################################################################################################################


# This structure stores the transition probability between tags 
# Format: {'start_tag': {'to_tag1': count, 'to_tag2': count, 'total_count': total number of times start_tag is present}}
TransitionProbablity = {}
# This structure stores the Emission probability between tags and words  
#{'word' : {'tag1': count, 'tag2': count , 'total_count': total number of times word has occured}}
EmissionProbablity = {}
# This structure contains the tags present in the input.

TagsInInput = set()

###############################################################################################################################

# Functions
###############################################################################################################################
		
		


#processes the input file 
def ParseInput(file):
    file = open(file, 'r')
    for line in file:
        line = line.strip()
        
        tokens = line.split()
        
        prev_tag = 'q0'
        
        for token in tokens:
            word, tag = token.rsplit('/', 1)
            ComputeEmissionCounts(word, tag)
            ComputeTransitionCounts(prev_tag, tag)
            prev_tag = tag

		
#This function updates the emission and transition probability dictionary to change value from count to probability.
def Compute_TP_EP():
    

    TagCount = len(TagsInInput)

    #updating tp
    for key, value in TransitionProbablity.iteritems():
        total_count = value['total_count']
        del value['total_count']

        for tag, count in value.iteritems():
            value[tag] = (count+1)/float(total_count+TagCount)

        value['others'] = 1.0/(total_count+TagCount)

		
    for tag in TagsInInput:
        if tag not in TransitionProbablity:
            TransitionProbablity[tag] = {'others': 1.0/TagCount}
	
#updating ep
    for key, value in EmissionProbablity.iteritems():
        wordCount = value['total_count']
        del value['total_count']

        for tag, count in value.iteritems():
            value[tag] = float(count)/float(wordCount)

		
			

#This  function  Updates the transition probability  dictionary.
def ComputeTransitionCounts(tag1, tag2):
    #global TransitionProbablity
    if tag1 in TransitionProbablity:    
        if tag2 in TransitionProbablity[tag1]:
        
            TransitionProbablity[tag1][tag2] += 1
        
        else:
            TransitionProbablity[tag1][tag2] = 1
        
        TransitionProbablity[tag1]['total_count'] += 1
    
    else:
        TransitionProbablity[tag1] = {tag2: 1, 'total_count': 1}


#This  function updates the emission probability count dictionary.
def ComputeEmissionCounts(token, POS):  
   
    TagsInInput.add(POS)
    if token in EmissionProbablity:
        if POS in EmissionProbablity[token]:
            EmissionProbablity[token][POS] += 1
        
        else:
            EmissionProbablity[token][POS] = 1
        
        EmissionProbablity[token]['total_count'] += 1
    
    else:
        EmissionProbablity[token] = {POS: 1, 'total_count': 1}
			

import csv
			
###############################################################################################################################


# Main program
###############################################################################################################################

file = sys.argv[1]
ParseInput(file)
Compute_TP_EP()
filepointer = open('hmmmodel.txt', 'w')

FileW = csv.writer(filepointer, delimiter=',')

for token, TaggingInput in EmissionProbablity.iteritems():
	for tagVal, Stats in TaggingInput.iteritems():
        	FileW.writerow([token, tagVal, Stats])

			
FileW.writerow(['<emission_end>'])

for Prev, Dout in TransitionProbablity.iteritems():
        for tagVal, Stats in Dout.iteritems():
            FileW.writerow([Prev, tagVal, Stats])


filepointer.close()
###############################################################################################################################
