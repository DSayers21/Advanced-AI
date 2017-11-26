import numpy as np
################################################################################
                                    #Functions
################################################################################
def GetDomainSize(Array):
     UniqueInsts = {}
     for x in range(0, len(Array)):
         UniqueInsts[Array[x]] = Array[x]
         
     return len(UniqueInsts)
 
#Returns count of full group
def GetCount(Array, Value):
     CountTrue = {};
     for x in range(0, len(Array)):
         if Array[x] == Value:
             CountTrue[x] = Array[x]
     return CountTrue

#Returns count of sub-group against another full group
def GetCountDict(Dict, Array, Value):
     CountTrue = {};
     for x in range(0, len(Array)):
         if x in Dict:
             if Array[x] == Value:
                 CountTrue[x] = Array[x]
     return CountTrue
 
#Array of Arguments and Values
def MaxLiklihood(Arguments):
    Size = len(Arguments)
    #Get Top of equation
    TopSum = GetCount(Arguments[0][0], Arguments[0][1])
    for x in range(1, Size):
        TopSum = GetCountDict(TopSum, Arguments[x][0],  Arguments[x][1])
    TopSum = len(TopSum)+1
    
    #Get Bottom of equation
    BottomSum = 0    
    if Size == 1: #Incase only one
        BottomSum = Arguments[0][0]
    else:
        BottomSum = GetCount(Arguments[1][0], Arguments[1][1])
        for x in range(2, Size):
            BottomSum = GetCountDict(BottomSum, Arguments[x][0],  Arguments[x][1])
    BottomSum = len(BottomSum) + GetDomainSize(Arguments[0][0]) 
    
    #Calc Probability
    Prob = float(TopSum) / float(BottomSum)
    return Prob

################################################################################
#                  Auto Generate based on bayes net Functions
################################################################################
def GetVarNameAndValue(String):
    Var = {}
    Var["Name"] = String.split("=",1)[0]  #Variable Name
    Var["Value"] =  String.split("=",1)[1] #Variable Value
    return Var
    
def AddToBayesNet(BayesNet, Key, Prob):
    BayesNet[Key] = Prob
    
def PrintBayesNet(BayesNet, Padding):
    for x in range(0, len(BayesNet.keys())):
        Test = '{0:' + str(Padding) + '}  {1}'
        print Test.format(BayesNet.keys()[x], BayesNet.values()[x])

def LearnParamenters(BayesNet, BayesNetVars):
    for key in BayesNet.keys():
    #for x in range(0, len(bn.keys())):
        CurrentKey =  key
        EqualsCount = CurrentKey.count('=')
        Vars = []
        if EqualsCount == 1:  #Case with one variable
            Var = GetVarNameAndValue(CurrentKey) 
            
            Vars.append((BayesNetVars[Var["Name"]],  Var["Value"]))
            
            String = Var["Name"] + "=" + Var["Value"]
            AddToBayesNet(BayesNet, String, MaxLiklihood(Vars))
            #print [Var["Name"] + "=" + Var["Value"]]
        if EqualsCount == 2:  #Case with two variable
            VarBG = GetVarNameAndValue(CurrentKey.split("|",1)[0] ) 
            VarAG = GetVarNameAndValue( CurrentKey.split("|",1)[1] ) 
            
            Vars.append((BayesNetVars[VarBG["Name"]],  VarBG["Value"]))
            Vars.append((BayesNetVars[VarAG["Name"]],  VarAG["Value"]))
            
            String = VarBG["Name"] + "=" + VarBG["Value"] + "|" + VarAG["Name"] + "=" + VarAG["Value"]
            AddToBayesNet(BayesNet, String, MaxLiklihood(Vars))
            
        if EqualsCount == 3:  #Case with three variable
            VarBG = GetVarNameAndValue(CurrentKey.split("|",1)[0] ) 
            VarAG = GetVarNameAndValue(CurrentKey.split("|",1)[1].split(",",1)[0] ) 
            VarAA = GetVarNameAndValue(CurrentKey.split(",",1)[1] ) 
            
            Vars.append((BayesNetVars[VarBG["Name"]],  VarBG["Value"]))
            Vars.append((BayesNetVars[VarAG["Name"]],  VarAG["Value"]))
            Vars.append((BayesNetVars[VarAA["Name"]],  VarAA["Value"]))
            
            String = VarBG["Name"] + "=" + VarBG["Value"] + "|" + VarAG["Name"] + "=" + VarAG["Value"] + "," +  VarAA["Name"] + "=" + VarAA["Value"]
            
            AddToBayesNet(BayesNet, String, MaxLiklihood(Vars))
    PrintBayesNet(BayesNet, 40)
################################################################################
#                                   Input
################################################################################
Alarm       = ["true","false","true","false","false","false","true","true","false","true"]
Mary        = ["true","false","true","false","false","false","true","true","false","true"] 
John        = ["true","false","false","true","false","false","true","true","false","true"]
Burglary    = ["true","false","false","false","false","false","true","true","false","false"]
Earthquake  = ["false","false","true","false","false","false","false","false","true","true"]

bn = {}
bn["b=true"] = 0
bn["b=false"] = 0
bn["e=true"] = 0
bn["e=false"] = 0
bn["a=true|b=true,e=true"] = 0
bn["a=true|b=true,e=false"] = 0
bn["a=true|b=false,e=true"] = 0
bn["a=true|b=false,e=false"] = 0
bn["a=false|b=true,e=true"] = 0
bn["a=false|b=true,e=false"] = 0
bn["a=false|b=false,e=true"] = 0
bn["a=false|b=false,e=false"] = 0
bn["j=true|a=true"] = 0
bn["j=true|a=false"] = 0
bn["j=false|a=true"] = 0
bn["j=false|a=false"] = 0
bn["m=true|a=true"] = 0
bn["m=true|a=false"] = 0
bn["m=false|a=true"] = 0
bn["m=false|a=false"] = 0

BNvars = {}
BNvars["b"] = Burglary
BNvars["e"] = Earthquake
BNvars["a"] = Alarm
BNvars["j"] = John
BNvars["m"] = Mary
################################################################################
#                                   Workshop Test
################################################################################
Play    = [0,0,1,1,1,0,1,0,1,1,1,1,1,0]
#0 = Sunny 1 = Overcast 2 = Rainy
Outlook = [0,0,1,2,2,2,1,0,0,2,0,1,1,2]
Windy   = [0,1,0,0,0,1,1,0,0,0,1,1,0,1]

Vars = []
Vars.append((Outlook, 2))
Vars.append((Play, 0))
print "P(Outlook|Play): \t", MaxLiklihood(Vars)

Vars = []
Vars.append((Windy, 1))
Vars.append((Outlook, 2))
Vars.append((Play, 0))
print "P(Windy|Outlook, Play): \t", MaxLiklihood(Vars)
################################################################################
#                                   Task 1B
################################################################################
LearnParamenters(bn, BNvars)
























