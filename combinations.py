def find_all_comb(a, r):
    stack = [] 
    results = [] 
    for i in a:
        stack.append([i]) 
    
    while len(stack) != 0:
        v = stack.pop() 

        if len(v) == r:
            results.append(v)
            continue 

        for i in a:
            s = v.copy()
            s.append(i) 
            stack.append(s)

     
    return results 
