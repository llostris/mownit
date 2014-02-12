from math import exp
from random import random

max_iterations = 100000

##
# Simulated Annealing Function:
# * state0 - initial state
# * temp0 - initial temperature
# * cost_fcn - function we try to minimalize
# * neighbour - function generating a next state to evaluate
# * alpha - a rate at which we decrease temperature
# * obj_limit - (optional) a cost_fcn limit at which we stop annealing
##

def simulated_annealing(state0, temp0, cost_fcn, neighbour, obj_limit=None, alpha=0.99 ):
    
    # Inicjalizacja stanu poczatkowego, poczatkowej temperatury oraz najlepszego stanu
    s = state0
    t = temp0
    best_s = s
    best_cost = cost_fcn(best_s)
    cost = cost_fcn(s)
    
    i = 0
    
    while i < max_iterations :
        
        t = alpha * t # Decrease temperature
        s_n = neighbour(s)  # Propose a neighbour state
        cost_n = cost_fcn(s_n) # Calculate cost ( energy ) of a proposal
        
        # Evaluate proposed state:
        if cost_n < cost :
            # If a proposed state is better we always choose it
            s = s_n
            cost = cost_n
        else :
            # Otherwise with a set probability we either take it or not
            p = exp( - (( cost_n - cost ) / t))
            if random() <= p :
                s = s_n
                cost = cost_n
            else :
                s = s
        
        # If our new state is the best state so far, we save it
        if cost < best_cost :
            best_s = s
            best_cost = cost        
        
        if obj_limit is not None and cost == obj_limit :
            print 'Iterations: ', i
            break
    
        i = i + 1   # Zwiekszamy licznik petli
    else :
        print 'Iterations: ', max_iterations
    
    print 'Best cost: ', best_cost
    print 'For state: ', best_s
    return best_s, best_cost