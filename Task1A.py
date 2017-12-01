#Returns the value that the user enters
def GetValue():
    UserInput = raw_input("Please Enter a Value: -> ")  # Python 2
    return float(UserInput)

#P( d ) : prior probability of having a disease
#P( t | d ) : probability that the test is positive given the person has the disease
#P( ¬t | ¬d) : probability that the test is negative given the person does not have the disease

#d: the person has the disease
#t: the test is positive 
def RareDisease(PD, PTD, PNTND):
    #P(t|¬d) = 1 - P(¬t|¬d)
    PTND = float(1) - float(PNTND)
    #P(t)
    PT = (float(PTD) * float(PD)) + (float(PTND) * 1 - float(PD))
    #P(d|t)
    PDT = (float(PTD) * float(PD)) / float(PT)
    return PDT


print  "|			Advanced AI			|"
#Outputs the probability given the values the user enters
print "P(d|t): " +  str(RareDisease(GetValue(), GetValue(), GetValue()))