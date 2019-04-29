# kt-assignment1


### How to run:
    + available commands:
        +   n  for ngram, default n is 3
        +   s  for soundex
        +   sl for soundex levenshtein
        +   e  for edit distance
        +   rs for refined soundex

    + example command:
        +   python main.py n

    + change method in edit distance:
        + comment out 'method_name' in apply_edit_distance function to enable different distance calculation methods

### External Libraries used:
    
    + ngram
    + math
    + operator
    + Levenshtein
    + jellyfish 