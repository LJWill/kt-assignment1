import ngram
import sys
import time
import math
import operator
import Levenshtein as lv


def apply_lev_dist(misspell, dictionary):

    count  = 0
    result = []

    for mis_word in misspell:
        predict_words = []

        if mis_word not in dictionary:
            if '/' not in mis_word:
                for dict_word in dictionary:
                    similarity = lv.ratio(mis_word, dict_word) 
                    predict_words.append((mis_word, similarity))

                best_pred = sorted(predict_words, key=operator.itemgetter(1))[0]
                result.append(best_pred)

            else:
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

                pred_word = G.find(mis_word) if G.find(mis_word) else mis_word

                result.append(pred_word)

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
    if method == 'ngram':
        result = apply_ngram(misspell, dictionary)
    elif method == 'soundx':
        pass
    elif method == 'levenshtein_distance':
        result = apply_lev_dist(misspell, dictionary)
    elif method == 'weighted_levenshtein_distance':
        pass
    elif method == 'editx':
        pass

    return result

def main(argv):
    option = argv[1]
    option_dict = {
        'n'     : 'ngram',
        's'     : 'soundx',
        'ld'    : 'levenshtein_distance',
        'wld'   : 'weighted_levenshtein_distance',
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
