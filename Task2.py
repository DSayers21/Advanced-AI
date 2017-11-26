import numpy as np

def Markov( SeqArray , ProbDict):
    print VarList
    Next = np.matrix([[0.5], [0.5]])
    
    for x in SeqArray:
        Prev = Next
        Next = ProbDict[x] * ProbDict["T"].transpose() * Next
        print ProbDict[x], " * ", ProbDict["T"].transpose(), " * ", Prev, " = ", Next
        
    Answer = Next.sum()
    print Answer  

Probs = {}
Probs["T"] = np.matrix([[0.5, 0.5], [0.8, 0.2]])
Probs["Omama"] = np.matrix([[0.4, 0], [0, 0.1]])
Probs["Opapa"] = Probs["Omama"]
Probs["Opee"] = np.matrix([[0.1, 0], [0, 0.4]])
Probs["Opoo"] = Probs["Opee"]
Probs["S0"] = np.matrix([[0.5], [0.5]])

#Assignment
ProbsT2 = {}
ProbsT2["T"] = np.matrix([[0.75, 0.25], [0.25, 0.75]])
ProbsT2["OHot"] = np.matrix([[0.05, 0], [0, 0.45]])
ProbsT2["OFreeze"] = ProbsT2["OHot"]
ProbsT2["OWarm"] = np.matrix([[0.45, 0], [0, 0.05]])
ProbsT2["OCold"] = ProbsT2["OWarm"]
ProbsT2["S0"] = np.matrix([[0.5], [0.5]])

VarList = [];

#Input all elements
VarName = raw_input('Enter a variable name: ')
while(VarName != "fin"):
    VarList.append(VarName)
    VarName = raw_input('Enter a variable name: ')
    
Markov( VarList, ProbsT2)