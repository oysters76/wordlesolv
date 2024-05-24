#include <stdio.h> 
#include <stdbool.h> 

#define N 5 

const int ALL_COMB_COUNT = 3*3*3*3*3; 

const int RULE_NO    = 0; 
const int RULE_YES   = 1; 
const int RULE_MAYBE = 2; 
const int RULE_COUNT = 3; //number of rules possible 

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

bool is_char_in_word(Word * w, char c){
    for (int i = 0; i < N; i++){
        if (w->word[i] == c) return true; 
    }
    return false; 
}

bool does_word_match_rule(Word * w, Rule * r){
 bool does_match = true; 
 for (int i = 0; i < N; i++){
    if (!does_char_match_rule(w, r, i)) return false;  
 }
 return true;
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

int main(void){
   Combination combinations[ALL_COMB_COUNT];
   gen_all_combinations(combinations); 
   printf("helloworld!\n");
}