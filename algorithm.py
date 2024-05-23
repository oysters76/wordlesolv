from combinations import *
from structures import *  

def filterPool(words, rules, wordPool:WordProbPool):
    for w in words:
        can_add = True
        for position, letter in enumerate(w):             
            for r in rules:
                if (not r.check_rule(letter, position, w)):
                    can_add = False 
                    break
            if not can_add:
                break 
        if can_add:
            wordPool.add(w, 0)

def calcProbabilities():
    pass 



def make_rules_from_word_and_rule_inds(word, rule_inds):
    rules = [] 
    word = str(word).lower() 
    for i, ind in enumerate(rule_inds):
        rules.append(FilterRule(word[i], i, ind))  
    return rules 


def find_information_bits_in_word(word, all_words, rule_combinations):
    information = 0 
    for rule_comb in rule_combinations:
        rules = make_rules_from_word_and_rule_inds(word, rule_comb)
        wordPool = WordProbPool(-1, -1, None, 0) 
        filterPool(all_words, rules, wordPool)
        expected_val = wordPool.get_information(len(all_words)) 
        information += expected_val 
    return information 


def get_all_rule_ind_combinations():
    a = [FilterRule.RULE_LETTER_CAN_BE_THERE, FilterRule.RULE_LETTER_SHOULD_BE_HERE, FilterRule.RULE_LETTER_SHOULD_NOT_BE_HERE] 
    r = WordleBoard.WORD_SIZE 

    return find_all_comb(a,r)
        

def updateWordPool(wordPool:WordProbPool, rules, all_words, combinations):
    wordPool.clear()
    filterPool(all_words, rules, wordPool)
    rwords = wordPool.remainingWords.copy() 
    wordPool.clear() 
    for word in rwords:
        information = find_information_bits_in_word(word, rwords, combinations)
        wordPool.add(word, information)

