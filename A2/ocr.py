#!/usr/bin/env python3
#
# ./ocr.py : Perform optical character recognition, usage:
#     ./ocr.py train-image-file.png train-text.txt test-image-file.png
# 
# Author: Varun Miranda
# (based on skeleton code by D. Crandall, Oct 2018)
#

""" 
********************************************************************REPORT********************************************************************

NOTE: TRAINING FILE: We have used the part 1 training file - bc.train

Approach to solve the program:

1. Simplified:
    
a. The simplified model would require only emission probability to be computed

b. For each test letter, all the train letters are compared to check which is the closest match

c. Initially equal weightage was given when spaces match and when '*' match, the simple model
   yielded a lot of spaces, hence when '*' match the number of matched bits is increased by 1
   and when spaces match, the number of matched bits is increased by 0.1
   
d. With respect to the value of matched bits, the emission probabilities are calculated and stored
   in an array. Each element in an array corresponds to the test letter position and they will store
   a dictionary of the negative log of the probability values
   
e. The character that has the minimum cost value per test character will be printed


2.  Viterbi:

a. To generate the most likely sequence, viterbi would be the best algorithm

b. Here, along with emission probabilities, initial and transition probabilities would also be taken
   into consideration
   
c. To calculate initial and transition probabilities, we included the training text file from part 1
   of Assignment 3. The format of the file is sentence tuples having (word, POS, word, POS, ... )
   This would have been a potential problem as transitions from a letter to a space/full stop/comma for instance 
   will not feature in the transition probability character occurences. So these have been handled separately
   
d. For initial probabilities, each tuple in the train-text file corresponds to a sentence, 
   so the starting letter has been taken for each of these sentences and using its frequency, a probability
   value is calculated and stored in an array
   
e. To calculate transition probability, each character combination in words in the sentence is taken
   into account. In the test data if any one of the two characters are spaces then the maximum probability
   is taken as spaces will most likely be spaces due to scarcity of bits 
   
f. Also, if the present character is a '.' or ',' then also the maximum probability is taken. If any other character 
   combination isn't present, then the minimum probability is chosen

g. The viterbi table is then computed using these probabilities and backtracking is also implemented by dictionaries
   that consists of keys "prob" and "prev" the latter which points to the previous maximum probability
   
h. The sequence is therefore generated in reverse order after backtracking from the last character and so the string
   is reversed. The final answer that is being printed is the same as the viterbi sequence

3. Attempt to fix bugs in test-5-0 and test-15-0

a. The spaces in between the words are not properly recognized because of the noise in the image that resembles
   another character while calculating the emission probability

b. Tried giving a high value for the number of matched bits (0.075 to 0.32) for cases where the '*' bit is present in the test-image
   but a space bit is present in the train-image. Worked better for those two cases but performed worse in some other test cases i.e. test-8-0

c. Also tried to forcefully give spaces if the minimum of the negative log of the probability exceeds 1750 (as this implies that very less bits matched). 
   This however yielded poor results for test-1-0 as almost all characters have the minimum negative log above 1750.

d. Very few of the test cases had an error of one character because in "Appeala" for instance, the transition probability from l to a exceeds the
   transition probability from l to s so "Appeala" did not change to "Appeals".

4. Time taken to run the code on silo: from 5s to 15s

********************************************************************REPORT********************************************************************
"""

#Part 1: Library Files

from PIL import Image, ImageDraw, ImageFont
import sys
import math

#Part 2: Starter Code

CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25
TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "

def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return result

def load_training_letters(fname):
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }

(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)

#Part 3: Initial Probability

filename=open(train_txt_fname,'r').readlines()
word=[]
ip = {}

#Taking data as tuples where each tuple is a sentence
#Word would be each word in a sentence without the parts of speech from the training file

for line in filename:
    data = tuple([w for w in line.split()])
    word += [data[0::2]]

#The starting character of each tuple will contain the starting letter of each sentence
#Storing that in an array

start_of_sentence = []
        
for w in range(0,len(word)):
    for l in word[w][0]:
        start_of_sentence.append(l)
        break

#Computing the frequencies of each character in the start of sentence array and storing them
#as initial probabilities in the dictionary "ip"        

def frequency(string):
    dictionary = {}
    for freq in string:
        char = dictionary.keys()
        if freq in char:
            dictionary[freq] += 1
        else:
            dictionary[freq] = 1
    return dictionary

letter_count = frequency(start_of_sentence)

for i in letter_count:
    ip[i] = float(letter_count[i])/sum(letter_count.values())
    
#Part 4: Transition Probability

transition = []
tp = {}

#For each word in the sentence, all possible two letter combinations are extracted and
#their probabilities are computed and stored in the dictionary "tp"
        
for i in range(0,len(word)-1):
    for j in range(0,len(word[i])-1):
        for k in range (0,len(word[i][j])-1):
            transition.append(word[i][j][k].lower()+ word[i][j][k+1].lower())

transition_count = frequency(transition)

for i in transition_count:
    tp[i] = float(transition_count[i])/sum(transition_count.values())
    
    #Here as each sentence was previously converted into lower case, we define the same
    #probability values for upper case and sentence case so "it", "It" and "IT" 
    #for instance will each have the same probability
    
    tp[i.upper()] = tp[i]
    tp[i.capitalize()] = tp[i]

#Part 5: Emission Probability and Simple Printing

ep = [0]*len(test_letters)
letter_max = [0]*len(test_letters) 

#Tuning parameter t is defined as 0.01

t = 0.01
for k in range(0,len(test_letters)):
    em_char = {}
    max_ct = 0
    for s in TRAIN_LETTERS:
        correct = 0
        total = 0
        all_spaces = 0
        for i in range(0,24):
            for j in range(0,13):
                
                #If both elements in the test and train matrix match they are given
                #different weightage as it is far more essential that the '*' match
                
                if test_letters[k][i][j] == train_letters[s][i][j] == '*':
                    correct+=1
                    total+=1
                elif test_letters[k][i][j] == train_letters[s][i][j] == ' ':
                    correct+=0.1
                    total+=1
                else:
                    total+=1
        
        #Calculating and storing the emission probabilities of each training character
        
        em_char[s] = - correct * math.log(1-t,2) - (total-correct) * math.log(t,2)
        if correct > max_ct:
            max_ct = correct
            letter_max[k] = s
    
    #All of the emission probabilies of length of the test string times the length of the train
    #string will be stored in "ep" which is an array of arrays
        
    ep[k] = em_char

#Simple sequence
    
print ("Simple:","".join([r for r in letter_max]))

#Part 6: Viterbi

#Example of the nomenclature used
#Character 'a' will yield

#Emission probability
#e1 = ep[0]['a']

#Initial probability
#w = ip['a']

#Viterbii first sequence
#v[0]['a'] = w * e1

v = [''] * len(test_letters)

#Initial Viterbi values

v[0] = {}

for s in TRAIN_LETTERS:   
    e1 = ep[0][s]
    if s not in ip.keys():
        w = min(ip.values())
    else:
        w = ip[s] 
        
    #Viterbi table will not only store the probabilities, it will also
    #store "prev" that will contain the most likely previous character
    
    v[0][s] = {"prob": - math.log(w,2) + e1, "prev": None}

#Next set of Viterbi values - use the Viterbi formula

for t in range(1,len(test_letters)):    

    v[t] = {}    

    for c in TRAIN_LETTERS:
        min_neglog = float("Inf")
        trace = ""
        for p in TRAIN_LETTERS:
            
            #Handling spaces, commas and full stops
            
            if p == " " or c == " " or c == "." or c == ",":
                prob = v[t-1][p]["prob"] - math.log(max(tp.values()),2)
            
            #Handling transition probabilities that didn't exist in the training text file
            
            elif (p+c) not in tp.keys():
                prob = v[t-1][p]["prob"] - math.log(min(tp.values()),2)
            
            #Remaining cases
            
            else:
                prob = v[t-1][p]["prob"] - math.log(tp[p+c],2)
            if prob < min_neglog:
                min_neglog = prob
                trace = p
                
        e = ep[t][c]
        v[t][c] = {"prob": min_neglog + e, "prev": trace}
        

#Getting the Viterbi sequence in reverse order by backtracking using the "prev" key

sentence = ""
last_char = ""
minimum = float("Inf")
t = len(test_letters)-1

for s in TRAIN_LETTERS:
    if v[t][s]["prob"] < minimum:
        minimum = v[t][s]["prob"]
        last_char = s

sentence += last_char
backtrack = v[t][last_char]["prev"]
        
for t in range(len(test_letters)-2,-1,-1):
    sentence += backtrack
    backtrack = v[t][backtrack]["prev"]

#Reversing the reversed string will get the ordered Viterbi sequence

sentence = sentence[::-1]

print("Viterbi:",sentence)
print("Final Answer:",sentence)

