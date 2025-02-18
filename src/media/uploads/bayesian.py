# CS 465
# Bayesian Network Queries

from probability import BayesNet, BayesNode # This program only uses the BayesNet structure.
# Probably don't need to import BayesNode, as it's used by BayesNet

T, F = True, False # T and F are used for True and False to simplify the creation of the BayesNet

# BayesNet as defined in the project documentation
network = BayesNet([
    ('A', '', 0.87),
    ('B', '', 0.62),
    ('C', 'A B', {(T, T): 0.18, (T, F): 0.06, (F, T): 0.98, (F, F): 0.35}),
    ('D', 'C', {(T): 0.46, (F): 0.03}),
    ('E', '', 0.95),
    ('F', '', 0.29),
    ('G', 'D E F', {(T, T, T): 0.32, (F, T, T): 0.01, (T, F, T): 0.48, (F, F, T): 0.07, (T, T, F): 0.21, (F, T, F): 0.45, (T, F, F): 0.76, (F, F, F): 0.19}),
    ('H', 'G', {(T): 0.28, (F): 0.79}),
    ('I', 'C', {(T): 0.12, (F): 0.34}),
    ('J', 'C', {(T): 0.91, (F): 0.56})])


def getNode(n): # getNode returns the BayesNode instance associated with the variable name, n 
    for node in network.nodes: # simple linear search algorithm that checks every node in the network until it finds a match
        if n == node.variable:
            return node # return found node


query = input('Enter Query: ') # Get input from user
values = query.split(',') # Seperate the query into the tuples using the commas

tuples = [] # Initilize empty list to store the pairs of node variables and thier query values
for pair in values:
    pair = pair.replace(" ", "") # Remove spaces from pairs just in case that's an issue
    t = pair.split("=") # Seperate node id from value
    tuples.append(tuple(t)) # Append node and value pair as tuple

node_values = {} # initilize node_value dictionary to store queried nodes and their T/F value

# These two lines updates node_values with the values in the tuples list
for t in tuples:
    node_values[t[0]] = t[1] # t[0] is the variable name and t[1] is the T/F value

#print(node_values)

running_prob = 1 # Running total of probability (chain rule)

def nodeValToTruth(value): # The input from the keyboard store True and False as strings, this function converts those string to T/F respectively
    return True if value in [True, 'True'] else False

# createAllNodeCombinations returns a list of dictionaries that contains every T/F combination of a given list of nodes (l).
# This function is important for marginalizing when not all parent node values are known
def createAllNodeCombinations(l):

    if not l:  # recursion base case: returns an empty dictionary in a list
        return [{}]
    
    p = createAllNodeCombinations(l[1:]) # recursive step on remaining nodes, uses a list with the front variable removed

    workingDictionaries = [] # creates the working list of dictionaries
    
    for d in p: # append true and false combinations for each dictionary
        workingDictionaries.append({l[0]: T, **d}) # Appends the first element of the current list and maps it to T 
        workingDictionaries.append({l[0]: F, **d}) # Appends the first element of the current list and maps it to F

    return workingDictionaries # return list of dictionaries


def definedParents(n): # returns if a given node (variable name) has all its parent's defined. Useful for discovering if marginalization is needed or not
    
    node = getNode(n) # retrieve node structure from variable name
    allParents = T # init flag to true
    
    for parent in node.parents: # interate over all parent nodes
        if parent not in node_values.keys(): # if the parent node has no recorded values, end the loop and return F
            allParents = F
            break
    return allParents # if all parents were discovered in the recorded values, then return T



# Main function of the program that retrieves / calculates values for evidence

# --------------------------------------------------------------
# The evidence argument is an artifact from when this function was designed to be recursive
# Evidence defaults to the saved node_values dictionary
# --------------------------------------------------------------
def getNodeProbablility(n, val, evidence=node_values): # gets node probability for a node, n (variable name), and T/F value
    
    node = getNode(n) # retrieves node structure using varaible name

    if definedParents(n): # check if the node has all of it's parents defined (can I just look up the value?)
        # -----------------------------------------------------
        # nodeValToTruth used to ensure that T/F are always treated as booleans and not strings
        # ------------------------------------------------------
        parentVals = {parent: nodeValToTruth(evidence[parent]) for parent in node.parents} # Create mapping of parents to their saved values
        return node.p(nodeValToTruth(val), parentVals)  # Looks up value using the parent value dictionary

    else: # if a parent is missing for a node, the value has to be marginalized 

        runningSum = 0 # initilize variable to save the sum of calculated prbabilites

        missingVars = [node_.variable for node_ in network.nodes if node_.variable not in evidence] # Creates a list of variable without recorded values

        allCombos = createAllNodeCombinations(missingVars) # generate all T/F values among the missing variables 

        # ------------------------------------------------------------------------
        # Copying the value dictionary would've had a similar effect as the next three lines, but this ensures that no strings are used to represent booleans
        # This was a common issue during testing, so nodeValToTruth is used more than it probably needs to for safety
        # ------------------------------------------------------------------------
        recordedValues = {}  # Init recorded values dictionary for variables that we have input for
        for var, value in evidence.items(): # Iterate over every key-value pair
            recordedValues[var] = nodeValToTruth(value) # Copy over the value

        for assignment in allCombos:  # Iterate over all assignments
            finalAssignment = {**recordedValues, **assignment}  # Merges the two dictionaries, creating one dictionary that use both known and unknown values
            
            prob = 1 # initial probability
            for node in network.nodes:  # Iterate over all nodes
                
                var = node.variable # Save the name of the variable
                
                parentVals = {parent: finalAssignment[parent] for parent in node.parents} # Create a list of the parent values from the assignment dictionary
                
                bool_value = nodeValToTruth(finalAssignment[var]) # Get the value of the current node in the current assignment dictionary
                prob *= node.p(bool_value, parentVals) # Multiply in the found value from the probability tables into the running probability

            runningSum += prob  # Add newly calculated probability from the current assignment dicitonary to the current sum

        return runningSum # Return the entire sum of all the assignments 


for t in tuples: # Iterate over all queries

    prob = getNodeProbablility(t[0], nodeValToTruth(t[1])) # Find the node probability using the data from the current query
    
    running_prob *= prob # Multiply in the calculated value into the running probability (chain rule) 

print(running_prob) # print the final result