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

def updateWordPool(wordPool:WordProbPool, rules, all_words):
    wordPool.clear()
    filterPool(all_words, rules, wordPool)
