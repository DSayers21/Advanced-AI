import numpy as np
import random
###############################################################################
Testbn = {}
Testbn["b=true"] = 0.001
Testbn["b=false"] = 0.999
Testbn["e=true"] = 0.002
Testbn["e=false"] = 0.998
Testbn["a=true|b=true,e=true"] = 0.95
Testbn["a=true|b=true,e=false"] = 0.94
Testbn["a=true|b=false,e=true"] = 0.29
Testbn["a=true|b=false,e=false"] = 0.001
Testbn["a=false|b=true,e=true"] = 0.05
Testbn["a=false|b=true,e=false"] = 0.06
Testbn["a=false|b=false,e=true"] = 0.71
Testbn["a=false|b=false,e=false"] = 0.999
Testbn["j=true|a=true"] = 0.90
Testbn["j=true|a=false"] = 0.05
Testbn["j=false|a=true"] = 0.1
Testbn["j=false|a=false"] = 0.95
Testbn["m=true|a=true"] = 0.7
Testbn["m=true|a=false"] = 0.01
Testbn["m=false|a=true"] = 0.3
Testbn["m=false|a=false"] = 0.99
###############################################################################
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

Alarm       = ["true","false","true","false","false","false","true","true","false","true"]
Mary        = ["true","false","true","false","false","false","true","true","false","true"] 
John        = ["true","false","false","true","false","false","true","true","false","true"]
Burglary    = ["true","false","false","false","false","false","true","true","false","false"]
Earthquake  = ["false","false","true","false","false","false","false","false","true","true"]

BNvars = {}
BNvars["b"] = Burglary
BNvars["e"] = Earthquake
BNvars["a"] = Alarm
BNvars["j"] = John
BNvars["m"] = Mary
###############################################################################
class BayesNode:
   def __init__(self, Name, States, Parents):
       self.Parents = Parents   #Parents of the current node
       self.Name = Name
       self.States = States     #Potential Values e.g. true, false
       self.SampledState = ""
       
   def GetAllCombinations(self):
       List = []
       for x in range(0, len(self.States)):
           List.append(self.Name + "=" + self.States[x])
       return List
    
   #Returns the variable in the form varName=varState
   def GetGivenState(self, State):
       for x in range(0, len(self.States)):
           if self.States[x] == State:
               return self.Name + "=" + self.States[x]
    
   def SampleVariable(self, bn, Sample):
      SampledValue = None
      randnum = random.random()
    
      Value = None
      if len(self.Parents) == 0:
          Value = bn[self.GetGivenState("true")]
    
      else: #Has Parents
          ParentsString = ""
          for x in range(0, len(self.Parents)):
              CurrentParent = self.Parents[x]
              if CurrentParent.SampledState == "": #Hasnt Been Sampled yet
                  CurrentParent.SampleVariable(bn, Sample)
              ParentsString += CurrentParent.SampledState
              if x < len(self.Parents)-1:
                  ParentsString += ","

          BNKey = self.GetGivenState("true") + "|" + ParentsString
          Value = bn[BNKey]

      if randnum < Value: 
        SampledValue = self.GetGivenState("true")
      else:
        SampledValue = self.GetGivenState("false")
              
      self.SampledState = SampledValue
      Sample.append(SampledValue)
      return SampledValue
###############################################################################      
                            #PARAMATER LEARNING
###############################################################################
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

LearnParamenters(bn, BNvars)    
PrintBayesNet(bn, 40)

###############################################################################
                                #INFERENCE
###############################################################################
def RejectionSampling(QueryVar, ObservedVals, bn, BNVars, N):
    #Inputs
        #QueryVar       = the query variable
        #ObservedVals   = the observed values
        #bn             = A Baesian network
        #BNVars         = the variables of the bayesian network with parent 
        #                 relationships
        #N              = the total number of samples to be performed
    
    #Do Sampling
    Sample = []
    GoodSamples = []
    for x in range(0,N):
        Sample = []
        for elem in BNVars:
            elem.SampleVariable(bn, Sample)

        #See If Sample Conforms
        Stop = 1
        for y in ObservedVals:
            if y not in Sample:
                Stop = 0
        if Stop == 1: #Sample conforms
            GoodSamples.append(Sample)
    #End Do Sampling
    #All samples which match the observed values
    Counts = {}
    for Sample in GoodSamples:
        for elem in Sample:
            if QueryVar+"=" in elem:
                OnlyState = elem.split("=",1)[1]
                if OnlyState in Counts:
                    Counts[OnlyState] = Counts[OnlyState] + 1
                else:
                    Counts[OnlyState] = 1
    #Get total amount of good samples
    TotalGoodSamples = Counts["true"] + Counts["false"]
    
    NCounts = {}
    NCounts["true"] = float(Counts["true"])/float(TotalGoodSamples)
    NCounts["false"] = float(Counts["false"])/float(TotalGoodSamples)
    
    #print("After Norm =" + "<" + str(NCounts["true"]) + "," + str(NCounts["false"]) + ">")
    return NCounts
###############################################################################
#Bayes Net
B = BayesNode("b", ["true", "false"], [])
E = BayesNode("e", ["true", "false"], [])
A = BayesNode("a", ["true", "false"], [B, E])
M = BayesNode("m", ["true", "false"], [A])
J = BayesNode("j", ["true", "false"], [A])

BNVars = [B, E, A, M, J]

ObservedVals = []
ObservedVals.append("j=true")
ObservedVals.append("m=true")

Probs = RejectionSampling("b", ["j=true", "m=true"], bn, BNVars, 100000)
print("B|j=true,m=true")
print("After Norm =" + "<" + str(Probs["true"]) + "," + str(Probs["false"]) + ">")
print("TESTING NETWORK")
Probs = RejectionSampling("b", ["j=true", "m=true"], Testbn, BNVars, 100000)
print("B|j=true,m=true")
print("After Norm =" + "<" + str(Probs["true"]) + "," + str(Probs["false"]) + ">")
###############################################################################