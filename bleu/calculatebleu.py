import codecs
import os
import sys
import math

#functions

def process_directory(input):
    '''
    stores the files in the given path to a structure and returns this structure
    '''
    filesList = list()
    for file in os.listdir(input):
        fn = os.path.join(input, file)
        file_text = generate_tokens(fn)

        filesList.append(file_text)

    return filesList




def generate_tokens(path):

    input = []

    myfile = codecs.open(path, 'r', encoding='utf-8')

    for sentence in myfile:
        token = sentence.strip().split()
        input.append(token)

    return input

def Compute_brevity_penality(input_sentence, ref_input__sentence):

    '''
    Computes brevity penality values based on the given candidate and refrence folder.
    '''

    length_of_cand = 0
    length_of_ref = 0


    for mykey, current_sentence in enumerate(input_sentence):
        current_reference_len = 0
        minimum_ref = sys.maxint

        length_of_cand += len(current_sentence)

        for ref_sentence in ref_input__sentence:

            if abs(len(ref_sentence[mykey])-len(current_sentence)) < minimum_ref:

                minimum_ref = len(ref_sentence[mykey])-len(current_sentence)

                current_reference_len = len(ref_sentence[mykey])

        length_of_ref += current_reference_len
    #computes bp based on the candidate and reference lengths

    if length_of_cand>length_of_ref:
        bp = 1.0
    else:
        bp =  math.exp(1.0 - float(length_of_ref)/length_of_cand)

    return bp



def DictionaryUpdater(my_input1, my_input2):
    '''
    loops over the my_input2 and calculates clip counts based on my_input1
    '''

    for k, v in my_input2.iteritems():
        if k not in my_input1:
            my_input1[k] = v
        else:
            my_input1[k] = max(v, my_input1[k])



def generate_ngrams(line, n=1):
    '''
    Generates n grams and updates count in the respective dictionary
    '''

    local_dict = {}

    for value in xrange(0, len(line)-n+1):
        n_gram = tuple(line[value: value+n])
        #update_dict_counts(local_dict, n_gram)
        if n_gram in local_dict:
            local_dict[n_gram] += 1
        else:
            local_dict[n_gram] = 1


    return local_dict


def bleu_score(sentence_data, reference_data):
    penalty = Compute_brevity_penality(sentence_data, reference_data)
    tbleu = 0

    for ngram_value in xrange(1, 5):
        clipCounts = 0
        candidate_count = 0

        for key, sentence in enumerate(sentence_data):
            local_ngram = {}

            for reference in reference_data:
                temp_dict = generate_ngrams(reference[key], ngram_value)
                DictionaryUpdater(local_ngram,temp_dict)

            sentence_ngram = generate_ngrams(sentence, ngram_value)


            for k, v in sentence_ngram.iteritems():

                if k in local_ngram:
                    clipCounts += min(v, local_ngram[k])

            candidate_count += len(sentence) - ngram_value + 1


        ratio = clipCounts/float(candidate_count)
        log_val = (math.log(ratio))/float(4)
        tbleu+=log_val
    bleu_score =  math.exp(tbleu)*penalty

    return bleu_score




#main
reference_input = sys.argv[2]
candidate_file = sys.argv[1]
input_candidate_data = generate_tokens(candidate_file)


if os.path.isdir(reference_input):
        reference_data = process_directory(reference_input)
else:
        reference_data = list()
        reference_data.append(generate_tokens(reference_input))

BLEU = bleu_score(input_candidate_data, reference_data)
#print "bleu score is "+BLEU

result = open('bleu_out.txt', 'w')

result.write('%s' % BLEU)

result.close()