from ctypes import *

N = 5 
MAX_WORD_COUNT = 14000 
MAX_RULES_COUNT = 10 

class Combination(Structure):
    _fields_ = [("comb", c_int * N),
                ("count", c_int)]

class Word(Structure):
    _fields_ = [("word", c_char * N)]

class Rule(Structure):
    _fields_ = [("w", Word),
                ("combi", Combination)]

class WordPool(Structure):
    _fields_ = [("words", Word * MAX_WORD_COUNT),
                ("count", c_int)]

class RulePool(Structure):
    _fields_ = [("rules", Rule * MAX_RULES_COUNT),
                ("count", c_int)]