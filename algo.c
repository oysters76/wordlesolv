#include <stdio.h> 
#include <stdbool.h> 

#define N 5 
#define MAX_WORD_COUNT 14000 
#define MAX_RULES_COUNT 10 

const int ALL_COMB_COUNT = 3*3*3*3*3; 

#define RULE_NO    0 
#define RULE_YES   1 
#define RULE_MAYBE 2 
#define RULE_COUNT 3 //number of rules possible 

typedef struct Combination{
    int comb[N];
    int count;
} Combination; 

typedef struct Word{
    char word[N];
} Word; 

typedef struct Rule{
    Word w; 
    Combination combi; 
} Rule; 

typedef struct WordPool{
    Word words[MAX_WORD_COUNT]; 
    int count; 
} WordPool; 

typedef struct RulePool{
    Rule rules[MAX_RULES_COUNT]; 
    int count;
} RulePool;

bool is_char_in_word(Word * w, char c){
    for (int i = 0; i < N; i++){
        if (w->word[i] == c) return true; 
    }
    return false; 
}

bool does_char_match_rule(Word * w, Rule * r, int position){
    char c = w->word[position]; 
    char actual_c = r->w.word[position];
    switch (r->combi.comb[position]){
        case RULE_NO:{
            return !is_char_in_word(w,c);  
        }
        case RULE_YES:{
            return c == actual_c; 
        }
        case RULE_MAYBE:{
            return is_char_in_word(w, c); 
        }
    }
    return false; 
}

bool does_word_match_rule(Word * w, Rule * r){
 for (int i = 0; i < N; i++){
    if (!does_char_match_rule(w, r, i)) return false;  
 }
 return true;
}


Combination copy_comb(Combination c){
    Combination v; 
    for (int i = 0; i < N; i++) 
        v.comb[i] = c.comb[i];
    v.count = c.count; 
    return v;  
}

void gen_all_combinations(Combination * combinations){
    Combination stack[ALL_COMB_COUNT]; 
    int p = 0; 
    int ind = 0; 
    for (int i = 0; i < RULE_COUNT; i++){
        Combination c;
        c.comb[0] = i; 
        c.count = 1;
        stack[p++] = c; 
    }
    while (p > 0){
        p--; 
        Combination c = stack[p]; 
        if (c.count == N){
            combinations[ind++] = copy_comb(c);             
            continue; 
        }
        for (int i = 0; i < RULE_COUNT; i++){
            Combination v = copy_comb(c);
            v.comb[v.count++] = i;
            stack[p++] = v;
        }
    }
}

void filter(WordPool * all_words, WordPool * filtered_words, RulePool * rulePool){
    for (int i = 0; i < all_words->count; i++){
        Word w = all_words->words[i]; 
        bool can_add = true; 

        for (int j = 0; j < N; j++){
            for (int r = 0; r < rulePool->count; r++){
                Rule rule = rulePool->rules[r];  
                if (!(does_word_match_rule(&w, &rule))){
                    can_add = false; 
                    break;
                }
            }
            if (!can_add){
                break; 
            }
        }
        if (can_add){
            filtered_words->words[filtered_words->count++] = w; 
        }
    }
}

int main(void){
    return 0; 
}