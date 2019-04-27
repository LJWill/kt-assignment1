import ngram
import sys
import time
import math
import operator
import Levenshtein as lv
import jellyfish as jf

def apply_soundex(misspell, dictionary):
    count  = 0
    result = []

    for mis_word in misspell:
        predict_words = []

        if mis_word not in dictionary:
            if '/' not in mis_word:
                for dict_word in dictionary:
                    soundex_mis  = jf.soundex(mis_word)
                    soundex_dict = jf.soundex(dict_word)
                    l_dist       = jf.levenshtein_distance(soundex_mis, soundex_dict)

                    predict_words.append((dict_word, l_dist))

                first_five_pred = sorted(predict_words, key=operator.itemgetter(1), reverse=False)[:5]
                pred_words = [x[0] for x in first_five_pred]

                result.append(pred_words)

            else:
                # do not predict when  word contains '/', a lazy method
                result.append(mis_word)

        # if mis_word in dictionary
        else:
            result.append(mis_word)
        
        count += 1
        print("Processing: {} / {}".format(count, len(misspell)), end='\r')


    return result


def apply_soundex_ngram(misspell, dictionary):
    count  = 0
    result = []

    soundex_dict = list(map(jf.soundex, dictionary))
    soundex_mis  = list(map(lambda x: {x:jf.soundex(x)}, misspell))
    # print(soundex_mis)

    G = ngram.NGram(soundex_dict)

    for (mis_word, s_mis) in misspell:
        if mis_word not in dictionary:
            if '/' not in mis_word:
                pred_words = []
                if G.search(s_mis, threshold = 0.4):
                    search_result = G.search(jf.soundex(mis_word), threshold = 0.4)

                    try:    search_result[0][1]
                    except: search_result = (mis_word, 1)
                    else:   highest_score = search_result[0][1]
                    
                    for (w,s) in search_result:
                        if math.isclose(s, highest_score):
                            pred_words.append(w)

                    if len(pred_words) == 1:
                        result.append(pred_words[0])
                    else:
                        result.append(pred_words)

            else:
                # do not predict when  word contains '/', a lazy method
                result.append(mis_word)

        # if mis_word in dictionary
        else:
            result.append(mis_word)
        
        count += 1
        print("Processing: {} / {}".format(count, len(misspell)), end='\r')

    return result


def apply_damerau_levenshtein(misspell, dictionary):
    count  = 0
    result = []

    for mis_word in misspell:
        predict_words = []

        if mis_word not in dictionary:
            if '/' not in mis_word:
                for dict_word in dictionary:
                    # dl_dist = jf.damerau_levenshtein_distance(mis_word, dict_word)
                    # jaro_dist = jf.jaro_distance(mis_word, dict_word)
                    # jw_dist = jf.jaro_winkler(mis_word, dict_word)
                    hamming_dist = jf.hamming_distance(mis_word, dict_word)

                    predict_words.append((dict_word, hamming_dist))

                first_five_pred = sorted(predict_words, key=operator.itemgetter(1), reverse=False)[:5]
                pred_words = [x[0] for x in first_five_pred]

                result.append(pred_words)

            else:
                # do not predict when  word contains '/', a lazy method
                result.append(mis_word)

        # if mis_word in dictionary
        else:
            result.append(mis_word)
        
        count += 1
        print("Processing: {} / {}".format(count, len(misspell)), end='\r')
    
    return result


def apply_lev_dist(misspell, dictionary):

    count  = 0
    result = []

    for mis_word in misspell:
        predict_words = []

        if mis_word not in dictionary:
            if '/' not in mis_word:
                for dict_word in dictionary:
                    similarity = lv.ratio(mis_word, dict_word) 
                    predict_words.append((dict_word, similarity))

                first_five_pred = sorted(predict_words, key=operator.itemgetter(1), reverse=True)[:5]
                pred_words = [x[0] for x in first_five_pred]

                result.append(pred_words)

            else:
                # do not predict when  word contains '/', a lazy method
                result.append(mis_word)

        # if mis_word in dictionary
        else:
            result.append(mis_word)
        
        count += 1
        print("Processing: {} / {}".format(count, len(misspell)), end='\r')
    
    return result


def apply_ngram(misspell, dictionary):
    G = ngram.NGram(dictionary)
    count  = 0
    result = []

    for mis_word in misspell:
        if mis_word not in dictionary:
            if '/' not in mis_word:
                """search a list of approximate words using ngram search"""
                
                pred_words = []
                if G.search(mis_word, threshold = 0.4):
                    search_result = G.search(mis_word, threshold = 0.4)

                    try:    search_result[0][1]
                    except: search_result = (mis_word, 1)
                    else:   highest_score = search_result[0][1]
                    
                    for (w,s) in search_result:
                        if math.isclose(s, highest_score):
                            pred_words.append(w)

                    if len(pred_words) == 1:
                        result.append(pred_words[0])
                    else:
                        result.append(pred_words)

                else:
                    result.append(G.find(mis_word))


            else:
                multi_words = mis_word.split('/')
                tmp = ''
                for w in multi_words:
                    if w:
                        approx_w = G.find(w)
                        tmp += (approx_w+'/')
                    elif len(w) == 3:   # for w is like /i/
                        tmp = w
                    else:
                        continue
                tmp = tmp[:-1]
                result.append(tmp)
        else:
            result.append(mis_word)

        count += 1
        print("Processing: {} / {}".format(count, len(misspell)), end='\r')

    
    return result


def predict(misspell, dictionary, method):
    if method == 'ngram':                           result = apply_ngram(misspell, dictionary)
    elif method == 'soundex':                       result = apply_soundex(misspell, dictionary)
    elif method == 'soundex ngram':                 result = apply_soundex_ngram(misspell, dictionary)
    elif method == 'levenshtein_distance':          result = apply_lev_dist(misspell, dictionary)
    elif method == 'damerau_levenshtein_distance':  result = apply_damerau_levenshtein(misspell, dictionary)
    elif method == 'editx':
        pass

    return result


def main(argv):
    option = argv[1]
    option_dict = {
        'n'     : 'ngram',
        's'     : 'soundex',
        'sn'    : 'soundex ngram',
        'ld'    : 'levenshtein_distance',
        'dld'   : 'damerau_levenshtein_distance',
        'e'     : 'editx'
    }

    # read input files and store them into list 
    with open('project_data/correct.txt') as f_correct:
        correct = f_correct.read().splitlines()
    with open('project_data/misspell.txt') as f_misspell:
        misspell = f_misspell.read().splitlines()
    with open('project_data/dict.txt') as f_dict:
        dictionary = f_dict.read().splitlines()

    
    if (option in option_dict.keys()):
        predict_result = predict(misspell, dictionary, option_dict.get(option))
    else:
        print("method not in scope")

    with open('output.txt', 'w') as f:
        for item in predict_result:
            f.write("%s\n" % item)



if __name__ == "__main__":
    main(sys.argv)
