###############################################################################
                                    #Imports
###############################################################################
import numpy as np
###############################################################################
                                    #Markov
###############################################################################
def Markov( SeqArray , ProbDict):
    #Inputs
        #SeqArray: List of events e.g. hot, cold etc.
        #ProbDict: Dictionary of the matrix probability tables for each event
    #Prints the sequence which has been entered by the user    
    print SeqArray
    #Creates the default Matrix with values 0.5 and 0.5
    Next = np.matrix([[0.5], [0.5]])
    #Loops over all the events in the sequence entered by the user
    for x in SeqArray:
        #Sets the previous to being next
        Prev = Next
        #Sets next the being the result of a matrix operation
            #Ot*T'*st-1
        Next = ProbDict[x] * ProbDict["T"].transpose() * Next
        #Prints the above operation
        print ProbDict[x], " * ", ProbDict["T"].transpose(), " * ", Prev, " = ", Next
    #Sets Answer to be the Sum of the final "Next" Matrix    
    Answer = Next.sum()
    #Prints the answer then returns it
    print Answer 
    return Answer
###############################################################################
                                    #Data Sets           
###############################################################################   
#Testing Data Set
Probs = {}
Probs["T"] = np.matrix([[0.5, 0.5], [0.8, 0.2]])
Probs["Omama"] = np.matrix([[0.4, 0], [0, 0.1]])
Probs["Opapa"] = Probs["Omama"]
Probs["Opee"] = np.matrix([[0.1, 0], [0, 0.4]])
Probs["Opoo"] = Probs["Opee"]
Probs["S0"] = np.matrix([[0.5], [0.5]])

#Assignment Data Sets
ProbsT2 = {}
ProbsT2["T"] = np.matrix([[0.75, 0.25], [0.25, 0.75]])
ProbsT2["OHot"] = np.matrix([[0.05, 0], [0, 0.45]])
ProbsT2["OFreeze"] = ProbsT2["OHot"]
ProbsT2["OWarm"] = np.matrix([[0.45, 0], [0, 0.05]])
ProbsT2["OCold"] = ProbsT2["OWarm"]
ProbsT2["S0"] = np.matrix([[0.5], [0.5]])
###############################################################################
                        #Get sequence of events from user
###############################################################################
#Init the VarList to a list type
VarList = [];
#Output instruction message to user
print "Type \"fin\" to finish your entered sequence." 
#Input all elements
VarName = raw_input('Enter a variable name: ')
while(VarName != "fin"):
    VarList.append(VarName)
    VarName = raw_input('Enter a variable name: ')
###############################################################################

###############################################################################
#Perform the markov model on the events the user has entered, using the passed
    #Set of probabilities
Markov( VarList, ProbsT2)
###############################################################################