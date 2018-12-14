#!/usr/bin/env python3
""" assign.py : Solve the Assign problem
 Summary of Citations : 
 https://stackoverflow.com/questions/19368375/set-partitions-in-python/30134039
 https://stackoverflow.com/questions/8280250/how-to-open-files-given-as-command-line-arguments-in-python
 https://stackoverflow.com/questions/22556449/print-a-list-of-space-separated-elements-in-python-3
--------------------------------------------------------------------------------------------------------"""

"Importing the necessary libraries"

import sys
import pandas as pd

"""The search problem involves the user to split the name array into all possible combinations of groups
[name1],[name2,name3];[name2],[name1,name3];[name3],[name1,name2];[name1,name2,name3];[name1],[name2],[name3] etc.
keeping in mind that there cannot be more than 3 people in one group 
https://stackoverflow.com/questions/19368375/set-partitions-in-python/30134039"""

def partition(collection):
    if len(collection) == 1:
        yield [collection]
        return

    first = collection[0]
    for smaller in partition(collection[1:]):
        for n, subset in enumerate(smaller):
            subarray = smaller[:n] + [[first] + subset]  + smaller[n+1:]
            if all (len(subarray[j]) <= 3 for j in range(0,len(subarray))):
                yield subarray
        yield [[first]] + smaller

"Reading the input files and reading the first column as names"

input = pd.read_csv(sys.argv[1],header = None, delimiter = ' ')
names = input[0].values.tolist()

"Solution function"

def solution():
    
    "assuming minimum cost can take any value, even a very high number the initial value is set to Inf"
    minimum_cost = float("Inf")
    
    "Keeping track of the number of combinations explored in the iterations variable"
    iterations = 0
    
    "As partition(names) is a generator function, p will not examine the entire list"
    "rather, partition(names) will be generated on the fly"
       
    for p in (partition(names)):
        
        sum_of_constants = 0
        sum_n_parameter = 0
        sum_m_parameter = 0
        
        "Iterating for all names"
        for name_index in range(0,len(names)):
            
            "Taking the n parameter as the value of the argument along times the number of preferences"
            "so that if the person finds a member in that list, the n parameter will get deducted"
            
            n_parameter = int(sys.argv[4]) * len(input[2][name_index].split(','))
            m_parameter = 0
        
            "Iterating for all groups in a combination"       
            for k in range (0,len(p)):
                if(names[name_index] in p[k]):
                    
                    "Updating n_parameter,m_parameter and constants"
                    for s in range(0,len(input[2][name_index].split(','))):
                        if input[2][name_index].split(',')[s] == '_' or input[2][name_index].split(',')[s] in p[k]:
                            n_parameter = n_parameter - int(sys.argv[4])
                    
                    for t in range(0,len(input[3][name_index].split(','))):
                        if input[3][name_index].split(',')[t] in p[k]:
                            m_parameter = m_parameter + int(sys.argv[3])
                    
                    if input[1][name_index]!= 0 and input[1][name_index]!= len(p[k]):
                        constant = 1
                    
                    else:
                        constant = 0
                
                else:
                    continue
            
            "For each combination, for one name, the sum of all the parameters are added"
            sum_of_constants = sum_of_constants + constant
            sum_n_parameter = sum_n_parameter + n_parameter
            sum_m_parameter = sum_m_parameter + m_parameter
        
        "Cost function computation for all the names"
        cost_function = len(p) * int(sys.argv[2]) + sum_of_constants + sum_n_parameter + sum_m_parameter
        iterations = iterations + 1
        
        "Update the minimum cost in case the cost function is lesser"
        if cost_function < minimum_cost:
            minimum_cost = cost_function
            array = p
            
        "Put a hard stop on the number of iterations, this number can be changed to get a more optimal solution"
        "but at a cost of more time"
           
        if(iterations >= 5000):
            return array, minimum_cost
    
    "In case before the iterlimit, the optimal solution is found"
    return array, minimum_cost

"Printing the solution in a printable format"    
answer = solution()
for i in answer[0]:
    print(*i)
print(answer[1])