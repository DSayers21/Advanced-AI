import numpy as np
################################################################################
                                    #Functions
################################################################################
def GetDomainSize(Array):
     UniqueInsts = {}
     for x in range(0, len(Array)):
         UniqueInsts[Array[x]] = Array[x]
         
     return len(UniqueInsts)
 
def GetDomainVars(Array):
     UniqueInsts = {}
     Vars = []
     for x in range(0, len(Array)):
         UniqueInsts[Array[x]] = Array[x]
         
     for key in UniqueInsts.keys():
         Vars.append(UniqueInsts[key])

     return Vars
 
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
                            #Inference by enumeration
################################################################################
def InferenceEnumeration(Statement, BayesNet, BayesNetVars, AssumedVal):

    #Get Variables
    Vars = []
    Vars.append(Statement.split("|",1)[0].split("(",1)[1].lower())
    Vars.append(Statement.split("|",1)[1].split(",",1)[0])
    
    EqualsCount = Statement.count(',') 
    
    for x in range(0, EqualsCount):
        if x == EqualsCount-1:
            Vars.append(Statement.split(",",1)[1].split(")",1)[0])
        else:
            Vars.append(Statement.split(",",1)[1].split(",",1)[0])
    print Vars
    #Check for the hidden variables
    HiddenVars = []
    for key in BayesNetVars.keys():
        Found = 0
        Current = key
        for x in range(0, len(Vars)):
            if Vars[x].lower() == Current: 
                Found = 1     
        if Found == 0:
            HiddenVars.append(Current) 
    print HiddenVars
    #End Check for the hidden variables    
    #Get the BN base variables without true or false values
    ProcessedBN = {}
    for key in BayesNet.keys():
        Statement1 = key
        EqualsCount = key.count('=')
        VarStruc = []
        VarStruc.append(Statement1.split("=",1)[0])
        if EqualsCount > 1:
            VarStruc.append(Statement1.split("|",1)[1].split("=",1)[0])
        #EqualsCount = Statement.count(,') 
        #print EqualsCount
        CommaCount = key.count(',')
        for x in range(0, CommaCount):
            VarStruc.append(Statement1.split(",",1)[1].split("=",1)[0])
        ProcessedBN[VarStruc[0]] = VarStruc
    print ProcessedBN
    #End Get the BN base variables without true or false values
    #Get the all the variables for the equation
    LinkBN = {}
    print "Test"
    for x in range(0, len(HiddenVars)):
        Position = -1
        Current = HiddenVars[x]
        for key in ProcessedBN.keys():
            Varables = ProcessedBN[key]
        
            if Current in ProcessedBN[key]:
                StringOC = Varables[0]
                for y in range(1, len(Varables)):
                    StringOC +=  Varables[y]
                LinkBN[StringOC] = Varables
                
    print LinkBN
    #Get the all the variables for the equation    
        
    #=P(b)[P(e)[P(a|b,e)P(j|a)P(m|a)]]    
    for x in range(0, len(HiddenVars)):
        Current = HiddenVars[x]
        CurrentVar = BayesNetVars[HiddenVars[x]]
        DomainSizeOfHidden = GetDomainSize(CurrentVar)
        #print DomainSizeOfHidden
        DomVars = GetDomainVars(CurrentVar)
        List = []
        for y in range(0, DomainSizeOfHidden):
           List.append((Current + "=" + DomVars[y]))
        #print List
        
    #Calculate
    def GetValue(CurrentEqu, Cur, Val):
        Output = ""
        for x in range(0, len(CurrentEqu)):
            if CurrentEqu[x] == Cur:
                Output += Cur + "=" + Val
        return Output
    
    #print "Loop Over: " + Cur
    FullList = []
    for key in LinkBN.keys():
        if len(LinkBN[key])>1:
            print LinkBN[key]
            CurrentEqu = LinkBN[key]
            EquationList = []
            HiddenSide = 1
            #Generate all hidden values
            for x in range(0, len(CurrentEqu)): 
                CurrentPos = CurrentEqu[x]
                VarFull = ""

                CurrentVar = BayesNetVars[CurrentPos]
                DomVars = GetDomainVars(CurrentVar)
                HiddenSide *= len(DomVars)
                #print DomVars
                for y in range(0, len(DomVars)):  

                    if CurrentPos in HiddenVars:
                        VarFull = CurrentPos + "=" + DomVars[y]
                    else:
                        if CurrentPos not in HiddenVars:
                            VarFull = CurrentPos + "=" + DomVars[y]
                    EquationList.append(VarFull)
            if len(EquationList) > 0:
                FullList.append(EquationList)
                print EquationList
    print FullList
    #Join
    MNA = FullList[0][0] + "|" + FullList[0][2]
    MA = FullList[0][1] + "|" + FullList[0][3]
    
    NABE = FullList[1][0] + "|" + FullList[1][2] + "," + FullList[1][4]
    ABE = FullList[1][1] + "|" + FullList[1][2] + "," + FullList[1][4]
    NABNE = FullList[1][0] + "|" + FullList[1][2] + "," + FullList[1][5]
    ABNE = FullList[1][1] + "|" + FullList[1][2] + "," + FullList[1][5]
    
    NANBE = FullList[1][0] + "|" + FullList[1][3] + "," + FullList[1][4]
    ANBE = FullList[1][1] + "|" + FullList[1][3] + "," + FullList[1][4]
    NANBNE = FullList[1][0] + "|" + FullList[1][3] + "," + FullList[1][5]
    ANBNE = FullList[1][1] + "|" + FullList[1][3] + "," + FullList[1][5]
    
    
    JNA = FullList[2][0] + "|" + FullList[2][2]
    JA = FullList[2][1] + "|" + FullList[2][3]
    
    MNA = BayesNet[MNA]
    MA = BayesNet[MA] 
    
    NABE = BayesNet[NABE]
    ABE = BayesNet[ABE]
    NABNE = BayesNet[NABNE]
    ABNE = BayesNet[ABNE]
    
    NANBE = BayesNet[NANBE]
    ANBE = BayesNet[ANBE]
    NANBNE = BayesNet[NANBNE]
    ANBNE = BayesNet[ANBNE]
    
    JNA = BayesNet[JNA]
    JA = BayesNet[JA]
    
    B = (ABE*JA*MA + NABE*JNA*MNA)+(ABNE*JA*MA + NABNE*JNA*MNA)
    NB = (ANBE*JA*MA + NANBE*JNA*MNA)+(ANBNE*JA*MA + NANBNE*JNA*MNA)
    
    Left = 1/(B+NB)*B
    Right = 1/(NB+B)*NB
    
    print Statement, "=", "<",Left,",", Right,">"
    
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


InferenceEnumeration("P(B|j,m)", bn, BNvars, "true")





















