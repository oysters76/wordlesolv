# Wordle Solver via Python 

Inspired by 3Blue1Brown's video on information theory.

## Demo 
Here's a quick demo of me using the solver to solve a the daily wordle problem: 

https://github.com/oysters76/wordlesolv/assets/75514064/e00f3c0a-0fa6-4f8a-bb28-5ca35097f4b0

## Building shared libraries 

In linux, 
```
    gcc -shared -o libfilter.so -fPIC algo.c
```

In Windows, 
```
 gcc -shared -o libfilter.dll algo.c
```

## Dependencies 
1. Pygame 2.5.2
