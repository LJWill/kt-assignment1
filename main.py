import ngram
import sys
import time
import math
import operator
import Levenshtein as lv
import jellyfish as jf


def create_refined_soundexdict():
    letter_groups = ["aehiouwy", "bp", "fv", "cks", "gj", "qxz", "dt", "l", "mn", "r"]
    rf_soundex_dict = {}
    i = 0
    for group in letter_groups:
        for c in group:
            rf_soundex_dict.update({c:i})
        i += 1

    return rf_soundex_dict

global rf_soundex_dict
rf_soundex_dict = create_refined_soundexdict()


def remove_adjacent_dup(stringObj):
    reduced_string = ''

    if len(stringObj) > 1:
        for i in range(0, len(stringObj)-1):
            if stringObj[i] != stringObj[i+1]:
                reduced_string += stringObj[i]
            else:
                continue

        reduced_string += stringObj[-1]

    else:
        return stringObj

    # remove all 0s
    reduced_string.replace('0', '')

    return reduced_string


def rf_string2soundex(stringObj):
    result = ''

    for letter in stringObj:
        if letter in rf_soundex_dict:
            num = str(rf_soundex_dict[letter])
        else:
            continue
        result += num

    return remove_adjacent_dup(result)


def apply_refined_soundex(misspell, dictionary):
    count  = 0
    result = []
    # soundex_dict_words = list(map(rf_string2soundex, dictionary))

    for mis_word in misspell:
        predict_words = []

        if mis_word not in dictionary:
            if '/' not in mis_word:
                for dict_word in dictionary:
                    dist = jf.damerau_levenshtein_distance(mis_word, dict_word)
                    if dist <= 2:
                        predict_words.append((dict_word, dist))
                    else:
                        continue

                new_pred_words = []
                for pw in predict_words:
                    similarity = jf.jaro_winkler(rf_string2soundex(pw), rf_string2soundex(mis_word))
                    new_pred_words.append((pw, similarity))
                    max_score = sorted(new_pred_words, key=operator.itemgetter(1), reverse=True)[0][1]

                if max_score != 0:
                    pred_words = [x[0] for x in new_pred_words if x[1] == max_score]
                    if len(pred_words) == 1:
                        result.append(pred_words[0])
                    else:
                        result.append(pred_words)
                else:
                    result.append(mis_word)


            else:
                result.append(mis_word)
        else:
            result.append(mis_word)

        count += 1
        print("Processing: {} / {}".format(count, len(misspell)), end='\r')

    return result

# soundex with levenshtein distance
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


def apply_soundex_levenshtein(misspell, dictionary):
    count  = 0
    result = []

    soundex_dict_words = list(map(jf.soundex, dictionary))
    soundex_mis_words  = list(map(jf.soundex, misspell))

    for (mis_word, s_mis) in zip(misspell, soundex_mis_words):
        predict_words = []
        if mis_word not in dictionary:
            if '/' not in mis_word:
                pred_words = []
                for (dict_word, s_dict) in zip(dictionary, soundex_dict_words):
                    dist = jf.levenshtein_distance(s_mis, s_dict)

                    if dist <= 1:
                        predict_words.append((dict_word, dist))
                    else:
                        continue

                    pred_word_list = sorted(predict_words, key=operator.itemgetter(1), reverse=False)
                    min_dist   = pred_word_list[0][1]
                    pred_words = [x[0] for x in pred_word_list if x[1] == min_dist]

                    result.append(pred_words)

                else:
                    result.append(mis_word)

            else:
                # do not predict when  word contains '/', a lazy method
                result.append(mis_word)

        # if mis_word in dictionary
        else:
            result.append(mis_word)
        
        count += 1
        print("Processing: {} / {}".format(count, len(misspell)), end='\r')

    return result


def apply_edit_distance(misspell, dictionary):
    count  = 0
    result = []
    method_name = 'damerau_levenshtein'
    # method_name = 'hamming'
    # method_name = 'jaro'
    # method_name = 'jaro_winkler'
    # method_name = 'levenshtein'

    for mis_word in misspell:
        predict_words = []

        if mis_word not in dictionary:
            if '/' not in mis_word:
                for dict_word in dictionary:
                    dist = jf.damerau_levenshtein_distance(mis_word, dict_word)
                    # dist = jf.hamming_distance(mis_word, dict_word)
                    # dist = jf.jaro_distance(mis_word, dict_word)
                    # dist = jf.jaro_winkler(mis_word, dict_word)
                    # dist = lv.ratio(mis_word, dict_word) 

                    predict_words.append((dict_word, dist))

                if method_name == 'damerau_levenshtein' or method_name == 'hamming':
                    # first word has the min distance
                    pred_word_list = sorted(predict_words, key=operator.itemgetter(1), reverse=False)
                    min_dist = pred_word_list[0][1]
                    pred_words = [x[0] for x in pred_word_list if x[1] == min_dist]

                    result.append(pred_words)

                elif method_name == 'jaro' or method_name == 'jaro_winkler' or  method_name == 'levenshtein':
                    # first word has the most similarity
                    pred_word_list = sorted(predict_words, key=operator.itemgetter(1), reverse=True)
                    max_score = pred_word_list[0][1]
                    pred_words = [x[0] for x in pred_word_list if x[1] == max_score]
                    
                    if max_score != 0:
                        pred_words = [x[0] for x in pred_word_list if x[1] == max_score]
                        if len(pred_words) == 1:
                            result.append(pred_words[0])
                        else:
                            result.append(pred_words)
                    else:
                        result.append(mis_word)
               

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
    if   method == 'ngram':                         result = apply_ngram(misspell, dictionary)
    elif method == 'soundex':                       result = apply_soundex(misspell, dictionary)
    elif method == 'soundex levenshtein':           result = apply_soundex_levenshtein(misspell, dictionary)
    elif method == 'edit_distance':                 result = apply_edit_distance(misspell, dictionary)
    elif method == 'refined soundex':               result = apply_refined_soundex(misspell, dictionary)

    return result


def main(argv):
    option = argv[1]
    option_dict = {
        'n'     : 'ngram',
        's'     : 'soundex',
        'sl'    : 'soundex levenshtein',
        'e'     : 'edit_distance',
        'rs'    : 'refined soundex'
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
