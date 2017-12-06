###############################################################################
                                    #Imports
###############################################################################
import random
###############################################################################
                                   #Data Sets
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

#Paramter Learning Values
BNvars = {}
BNvars["b"] = ["true","false","false","false","false","false","true","true","false","false"]
BNvars["e"] = ["false","false","true","false","false","false","false","false","true","true"]
BNvars["a"] = ["true","false","true","false","false","false","true","true","false","true"]
BNvars["j"] = ["true","false","false","true","false","false","true","true","false","true"]
BNvars["m"] = ["true","false","true","false","false","false","true","true","false","true"] 
###############################################################################
                                #Bayes Node Class
###############################################################################
class BayesNode:
   #Init Function
   def __init__(self, Name, States, Parents):
       #Inputs
           #Name:    Name of the bayes note
           #States:  All the potential states of the node e.g. True, false
           #Parents: List of parents of the node
        
       self.Parents = Parents   #Parents of the current node
       self.Name = Name         #Set Name
       self.States = States     #Potential Values e.g. true, false
       self.SampledState = ""   #Set SampledState to "" as hasnt been sampled yet
   #Returns all the combinations of the variable e.g. e=true, e=false etc.
   def GetAllCombinations(self):
       List = []
       #Loop over all states
       for x in range(0, len(self.States)):
           #Append the name of the node plus "=" and then the current state
           List.append(self.Name + "=" + self.States[x])
       #Return the list
       return List
   #Returns the variable in the form varName=varState
   def GetGivenState(self, State):
       #Input
           #State: A state of the variable e.g. true, false
       #Loop over all states
       for x in range(0, len(self.States)):
           if self.States[x] == State: #If the state is there
               return self.Name + "=" + self.States[x] #Return the name=state
   #Sample Variable function, samples the node
   def SampleVariable(self, bn, Sample):
       #Inputs
           #bn:      a bayes network
           #Sample:  the current list of sampled variables
      #Set SampledValue to a base value of None
      SampledValue = None
      #Generate a random number
      randnum = random.random()
      #Set Values to a base value of []
      Values = []
      #Check if the node has no paretns
      if len(self.Parents) == 0:
          #Set Value to the correct value from the bayesnet
          for x in self.States:
              Values.append((x, bn[self.GetGivenState(x)]))
          #print Values
              
      else: #Node has parent node or nodes
          #Set ParentsString to being empty
          ParentsString = ""
          #Loop over all the parents
          for x in range(0, len(self.Parents)):
              #Get the current parent
              CurrentParent = self.Parents[x]
              #Check if the current parent has been sampled
              if CurrentParent.SampledState == "": #Hasnt Been Sampled yet
                  #Sample the parent
                  CurrentParent.SampleVariable(bn, Sample)
              #Add the parents sampled state to the ParentsString
              ParentsString += CurrentParent.SampledState
              #If there is still more parents for the node
              if x < len(self.Parents)-1:
                  ParentsString += "," #Then add a comma to the parentsString
          #Set the BNKey to being the current nodes name plus value and also 
          #the parents string      
          for x in self.States:
              BNKey = self.GetGivenState(x) + "|" + ParentsString
              Values.append((x, bn[BNKey]))

      #Sort Values, to ensure the smallest is always at the front of the list
      Values = sorted(Values, key=lambda Values: Values[1])
      #Loop through all values, look for first time condition is met
      for x in range(0, len(Values)-1):
          #Check if the random number is less than value
          if randnum < Values[x][1]: 
            SampledValue = self.GetGivenState(Values[x][0]) #If less than set to cur pos
            continue
      #If Sampled Value never got set    
      if SampledValue == None: 
          SampledValue = self.GetGivenState(Values[len(Values)-1][0]) #Set to last element
          
      #Set SampledState to being the same as sampled value        
      self.SampledState = SampledValue
      #Append the current sampled value to the list of samples
      Sample.append(SampledValue)
      #Return the sampled value
      return SampledValue
###############################################################################      
                            #PARAMATER LEARNING
###############################################################################
def GetDomainSize(Array):
    #Inputs
        #Array of values e.g. true, false, false, true etc.
     UniqueInsts = {}
     #Looks for unique instances from the array
     for x in range(0, len(Array)):
         UniqueInsts[Array[x]] = Array[x]
     #Returns the length of the UniqueInsts
     return len(UniqueInsts)
 
#Returns count of full group
def GetCount(Array, Value):
     #Inputs
        #Array of values e.g. true, false, false, true etc.
        #Value is a state e.g. true or false
     CountTrue = {};
     #Loop over the array looking for where the value passed matchs a value in
     #the array
     for x in range(0, len(Array)):
         if Array[x] == Value:
             CountTrue[x] = Array[x] #Add the found value to the dictionary
     #Return the dictionary of elements
     return CountTrue

#Returns count of sub-group against another full group
def GetCountDict(Dict, Array, Value):
    #Inputs
        #Dict a dictionary representing a list of variables to also take 
            #into account
        #Array of values e.g. true, false, false, true etc.
        #Value is a state e.g. true or false
     CountTrue = {};
     #Loop over the array
     for x in range(0, len(Array)):
         if x in Dict: #If the current element is in the dictionary
             #Check if the current position is the same as value
             if Array[x] == Value:
                 CountTrue[x] = Array[x] #Add the found value to the dictionary
     #Return the dictionary of elements
     return CountTrue
 
#Array of Arguments and Values
def MaxLiklihood(Arguments):
    #Inputs
        #Arguments is an a list of list in the form [[a,true][b,false]] etc
    #Get the size of arguments
    Size = len(Arguments)
    #Equation of max likihood is
    #count(x|y,z)+1     /   count(y,z)+|X|
    
    #Get Top of equation
    #Get the sum of the first var given the second
    TopSum = GetCount(Arguments[0][0], Arguments[0][1])
    #Loop over arguments to find results that match all cases
    for x in range(1, Size):
        TopSum = GetCountDict(TopSum, Arguments[x][0],  Arguments[x][1])
    #Get the length of the dict representing all matches, then add one to it
    TopSum = len(TopSum)+1
    
    #Get Bottom of equation
    BottomSum = 0    
    if Size == 1: #Incase only one
        BottomSum = Arguments[0][0]
    else:
        #Get the sum of the first var given the second
        BottomSum = GetCount(Arguments[1][0], Arguments[1][1])
        #Loop over arguments to find results that match all cases
        for x in range(2, Size):
            BottomSum = GetCountDict(BottomSum, Arguments[x][0],  Arguments[x][1])
    #Get the length of the dict representing all matches, then add 
    #The domain size of the first argument to it
    BottomSum = len(BottomSum) + GetDomainSize(Arguments[0][0]) 
    
    #Calculate the Probability
    Prob = float(TopSum) / float(BottomSum)
    #Return the probability
    return Prob

def GetVarNameAndValue(String):
    #Inputs
        #String represents the statement e.g. b=false
    Var = {}
    #Split the statement based on "=" then assign the halfs to the dict
    Var["Name"] = String.split("=",1)[0]  #Variable Name
    Var["Value"] =  String.split("=",1)[1] #Variable Value
    #Return the dictionary which will contain values such as:
    #Var["Name"] = b, Var["Value"] = false
    return Var
    
def AddToBayesNet(bn, Key, Prob):
    #Inputs
        #bn a bayes net
        #key a position in the bayes net
        #Prob a probability to assign the the place in the bayes net
    #Assign the prob the the key position in the bayes net
    bn[Key] = Prob

def PrintBayesNet(bn, Padding):
    #Inputs
        #bn a bayes net
        #Padding an amount to space out the print
    #Loop over all keys in the bayes net
    for x in range(0, len(bn.keys())):
        #Print out each place in the bn with its probability
        Test = '{0:' + str(Padding) + '}  {1}'
        print Test.format(bn.keys()[x], bn.values()[x])

def LearnParameters(BayesNet, BayesNetVars):
    #Inputs
        #BayesNet:      A bayesian network
        #BayesNetVars:  A dictionary representing the bayes net
    
    #Loop over all keys in the bayes net
    for key in BayesNet.keys():
        #Get the current position in the bayes net
        CurrentKey =  key
        #Get the number of "=" in the current position
        EqualsCount = CurrentKey.count('=')
        Vars = []
        if EqualsCount == 1:  #Case with one variable
            #Get the name and value from the current position
            Var = GetVarNameAndValue(CurrentKey) 
            #Add the variable to a list
            Vars.append((BayesNetVars[Var["Name"]],  Var["Value"]))
            #Store the name and "=" and value of the current position
            String = Var["Name"] + "=" + Var["Value"]
        if EqualsCount == 2:  #Case with two variable
            #Get the names and values from the current position
            VarBG = GetVarNameAndValue(CurrentKey.split("|",1)[0] ) 
            VarAG = GetVarNameAndValue( CurrentKey.split("|",1)[1] ) 
            
            #Add the variables to a list
            Vars.append((BayesNetVars[VarBG["Name"]],  VarBG["Value"]))
            Vars.append((BayesNetVars[VarAG["Name"]],  VarAG["Value"]))
            
            #Store the name and "=" and value of the current position
            String = VarBG["Name"] + "=" + VarBG["Value"] + "|" + VarAG["Name"] + "=" + VarAG["Value"]
            
        if EqualsCount == 3:  #Case with three variable
            #Get the names and values from the current position
            VarBG = GetVarNameAndValue(CurrentKey.split("|",1)[0] ) 
            VarAG = GetVarNameAndValue(CurrentKey.split("|",1)[1].split(",",1)[0] ) 
            VarAA = GetVarNameAndValue(CurrentKey.split(",",1)[1] ) 
            
            #Add the variables to a list
            Vars.append((BayesNetVars[VarBG["Name"]],  VarBG["Value"]))
            Vars.append((BayesNetVars[VarAG["Name"]],  VarAG["Value"]))
            Vars.append((BayesNetVars[VarAA["Name"]],  VarAA["Value"]))
            
            #Store the name and "=" and value of the current position
            String = VarBG["Name"] + "=" + VarBG["Value"] + "|" + VarAG["Name"] + "=" + VarAG["Value"] + "," +  VarAA["Name"] + "=" + VarAA["Value"]
            
        #Calc the maxliklihood and store in at the proper pos in the bayes net
        AddToBayesNet(BayesNet, String, MaxLiklihood(Vars))
###############################################################################
#Run the LearnParameters function with bn and BNVars
LearnParameters(bn, BNvars)    
#Print the bayes net after the parameters have been learned
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
    
    print "Doing Rejection Sampling"
    #Do Sampling
    Sample = []
    #GoodSamples = []
    Counts = {}
    #Loop through for number of samples wanting to generate
    for x in range(0,N):
        Sample = []
        #Sample all variables
        for elem in BNVars:
            elem.SampleVariable(bn, Sample)

        #See If Sample Conforms
        Stop = 1
        for y in ObservedVals:
            if y not in Sample:#Sample does not conform
                Stop = 0
        if Stop == 1: #Sample conforms
            #Go through each element in the sample
            for elem in Sample:
                #Check if QueryVar= is in the current element
                if QueryVar+"=" in elem:
                    #Get the state of the variable e.g. true or false
                    OnlyState = elem.split("=",1)[1]
                    #Add to the position in the counts dict
                    if OnlyState in Counts:
                        Counts[OnlyState] = Counts[OnlyState] + 1
                    else:
                        Counts[OnlyState] = 1
    #Get total amount of good samples
    TotalGoodSamples = 0
    for key in Counts.keys():
        TotalGoodSamples += Counts[key]
    #Setup normalised counts dict
    NCounts = {}
    #Store the corresponding positions in counts into NCounts after being 
    #divided by the TotalGoodSamples
    for key in Counts:
        NCounts[key] = float(Counts[key])/float(TotalGoodSamples)
    #Return the NCounts dictionary
    return NCounts
###############################################################################
#Setup Bayes Net with relations, using the bayesnet class above
B = BayesNode("b", ["true", "false"], [])
E = BayesNode("e", ["true", "false"], [])
A = BayesNode("a", ["true", "false"], [B, E])
M = BayesNode("m", ["true", "false"], [A])
J = BayesNode("j", ["true", "false"], [A])

#Samples = []
#A.SampleVariable(Testbn, Samples)
#print Samples
#Setup BNVars array which points to the above nodes
BNVars = [B, E, A, M, J]
#Setup list of observed values
ObservedVals = []
ObservedVals.append("j=true")
ObservedVals.append("m=true")
#Testing Network using bayesnet with known values
#Generate the probability of b given j and m are both true
#Probs = RejectionSampling("b", ["j=true", "m=true"], Testbn, BNVars, 1000000)
#Output the question
#print("B|j=true,m=true")
#Output the calculated probability
#print("After Norm =" + "<" + str(Probs["true"]) + "," + str(Probs["false"]) + ">")

#Bayes network with the learned values from parameter learning
#Generate the probability of b given j and m are both true
Probs = RejectionSampling("b", ["j=true", "m=true"], bn, BNVars, 1000000)
#Output the question
print("B|j=true,m=true")
#Output the calculated probability
print("After Norm =" + "<" + str(Probs["true"]) + "," + str(Probs["false"]) + ">")
###############################################################################