import sys


# correct
with open('project_data/correct.txt') as f:
    correct = f.read().splitlines()

# damerau levenshtein
with open('output/damerau_levenshtein.txt') as f:
    damerau_levenshtein = f.read().splitlines()

# levenshtein
with open('output/levenshtein.txt') as f:
   levenshtein = f.read().splitlines()

# hamming
with open('output/hamming.txt') as f:
    hamming = f.read().splitlines()

# jaro
with open('output/jaro.txt') as f:
    jaro = f.read().splitlines()

# jaro_winkler
with open('output/jaro_winkler.txt') as f:
    jaro_winkler = f.read().splitlines()

# ngram
with open('output/ngram.txt') as f:
    ngram = f.read().splitlines()

# ngram single preditct
with open('output/ngram_single_predict.txt') as f:
    ngram_single_predict = f.read().splitlines()

# soundex
with open('output/soundex.txt') as f:
    soundex = f.read().splitlines()

# soundex levenshtein
with open('output/soundex_lev.txt') as f:
    soundex_lev = f.read().splitlines()

def accuracy(pred_file, correct_file):
    total_predict = len(correct_file)
    right_num = 0
    result = 0.0

    for (predict, correct) in zip(pred_file, correct_file):
        if predict == correct:
            right_num += 1
    
    print('accuracy: ', right_num, total_predict)

    result = right_num / total_predict

    return round(result, 5)

def recall(pred_file, correct_file):
    total_predict = len(correct_file)
    right_num = 0
    result = 0.0

    for (predict, correct) in zip(pred_file, correct_file):
        # if predict is list
        if(predict[0] == '['):
            predict_words = predict[1:-1].replace('\'', '').split(', ')
            for pw in predict_words:
                if pw == correct: right_num += 1

                
        else:   # if predict is single word
            if predict == correct: right_num += 1

    print('Recall: ', right_num, total_predict)

    result = right_num / total_predict

    return round(result, 5)

def precision(pred_file, correct_file):
    total_predict = 0
    right_num = 0
    result = 0.0

    for (predict, correct) in zip(pred_file, correct_file):
        # if predict is list
        if(predict[0] == '['):
            predict_words = predict[1:-1].replace('\'', '').split(', ')
            for pw in predict_words:
                total_predict += 1
                if pw == correct: right_num += 1

                
        else:   # if predict is single word
            total_predict += 1
            if predict == correct: right_num += 1

    print('Precesion: ', right_num, total_predict)

    result = right_num / total_predict

    return round(result, 5)



def main(argv):
    print('===========================================================================')
    lev_precision = precision(levenshtein, correct)
    lev_recall    = recall(levenshtein, correct)
    print('levenshtein precision: ', lev_precision)
    print('levenshtein recall: ', lev_recall)

    print('--------------------------------------------------------------------------')

    dlev_precision = precision(damerau_levenshtein, correct)
    dlev_recall    = recall(damerau_levenshtein, correct)
    print('damerau levenshtein precision: ', dlev_precision)
    print('damerau levenshtein recall: ', dlev_recall)

    print('--------------------------------------------------------------------------')

    hamm_precision = precision(hamming, correct)
    hamm_recall    = recall(hamming, correct)
    print('hamming precision: ', hamm_precision)
    print('hamming recall: ', hamm_recall)

    print('--------------------------------------------------------------------------')

    jaro_precision = precision(jaro, correct)
    jaro_recall    = recall(jaro, correct)
    print('jaro precision: ', jaro_precision)
    print('jaro recall: ', jaro_recall)

    print('--------------------------------------------------------------------------')

    jw_precision = precision(jaro_winkler, correct)
    jw_recall    = recall(jaro_winkler, correct)
    print('jaro winkler precision: ', jw_precision)
    print('jaro winkler recall: ', jw_recall)

    print('--------------------------------------------------------------------------')

    ngram_precision = precision(ngram, correct)
    ngram_recall    = recall(ngram, correct)
    print('ngram precision: ', ngram_precision)
    print('ngram recall: ', ngram_recall)

    print('--------------------------------------------------------------------------')

    soundex_precision = precision(soundex, correct)
    soundex_recall    = recall(soundex, correct)
    print('soundex precision: ', soundex_precision)
    print('soundex recall: ', soundex_recall)

    print('--------------------------------------------------------------------------')

    soundex_lev_precision = precision(soundex_lev, correct)
    soundex_lev_recall    = recall(soundex_lev, correct)
    print('soundex levenshtein precision: ', soundex_lev_precision)
    print('soundex levenshtein recall: ', soundex_lev_recall)

    print('--------------------------------------------------------------------------')

    ngram_accuracy  =  accuracy(ngram_single_predict, correct)
    print(ngram_accuracy)

    print('===========================================================================')




if __name__ == "__main__":
    main(sys.argv)