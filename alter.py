import csv
import numpy as np
import re
from sympy.logic.boolalg import to_cnf, to_dnf
from sympy.logic import simplify_logic
from sympy.abc import a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z

file_name = input("Please enter a CSV Filename:  ")
#bottom up defining structures
#node
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return self.data
    

#defining linked list
class LinkedList:
    def __init__(self, nodes=None):
        self.head = None
        if nodes is not None:
            node = Node(data=nodes.pop(0))
            self.head =node
            for elem in nodes:
                node.next = Node(data=elem)
                node = node.next

    def __repr__(self):
        node = self.head
        nodes = []
        while node is not None:
            nodes.append(node.data)
            node = node.next
        nodes.append("None")
        return " -> ".join(nodes)

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next

    def add_last(self, node):
        if not self.head:
            self.head = node
            return
        for current_node in self:
            pass
        current_node.next = node

#compares to linked lists
def compareLists(listA, listB, decisionAttribute):
    attrA = []
    attrB = []
    differences = []
    for node in listA:
        attrA.append(node)
    for node in listB:
        attrB.append(node)
    #first check whether even the lists are equal length
    if(len(attrA)==len(attrB)):

        #check the decision attribute
        decision1 = attrA[decisionAttribute].data
        decision2 = attrB[decisionAttribute].data

        #if true done return 1 or Lambda
        if decision1 == decision2:
            return -1

        # otherwise return a list of the different attribute numbers
        elif (decision1 != decision2):
            for i in range(0, len(attrA)):
                if i == 0:
                    object1 = attrA[i]
                    object2 = attrB[i]
                elif i == decisionAttribute:
                    continue
                else:
                    obj1 = attrA[i].data
                    obj2 = attrB[i].data
                    # if the attributes are equal skip
                    if obj1 == obj2:
                        continue
                    #otherwise add them to the difference list
                    else:
                        differences.append(i)
            return differences


    #should never reach here since all lists should be equal
    else:
        print("Error should not be here!")



#create the matrix for a given DT and DA
def createMatrix(decisionTable, decisionAttribute):
    print("Creating the matrix...")
    matrix_size = len(decisionTable)-1
    print("...Square Matrix of size : ", matrix_size)
    finalMatrix = np.empty((matrix_size, matrix_size), object)
    for object1 in range(0, len(decisionTable)):
        for object2 in range(object1+1, len(decisionTable)):
            result = compareLists(decisionTable[object1], decisionTable[object2], decisionAttribute)
            if (isinstance(result, int)):
                #finalMatrix[object1][object2-1] = [result]
                finalMatrix[object1][object2-1] = result
            elif (len(result)==1):
                #finalMatrix[object1][object2-1] = result
                finalMatrix[object1][object2-1] = result[0]
            else:
                #finalMatrix[object1][object2-1] = result
                finalMatrix[object1][object2-1] = tuple(result)
    return finalMatrix

def createCNF(matrix):
    print("Creating the CNF...")
    totalCNF = ''
    counter = 0
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    matrix_size = (len(matrix)**2)
    ##
    row_elements=[]
    for x in np.nditer(matrix, ["refs_ok"]):
        element = x.tolist()
        print("On item : ", counter)
        print("Out of : ", matrix_size)
        counter+=1
        print("----------------------")
        if element is None:
            continue
        #lambdas are -1 skip them
        if element == -1:
            continue
        # if a single attribute in the matrix
        if isinstance(element, int):
            #row_elements.append(str(element))
            row_elements.append(alphabet[element-1])
        # otherwise a list of attributes
        else: 
            element_string = ""
            #
            newstring = (map(lambda x: alphabet[x-1], element))
            newstring = '|'.join(map(str, newstring))
            fix_string = "(" + newstring + ")"
            row_elements.append(fix_string)

    if len(row_elements)!= 0:
        remove_dupes = list(set(row_elements))
        # half = len(remove_dupes) // 2
        # left = "&".join(remove_dupes[:half])
        # right = "&".join(remove_dupes[half:])
        # new_statement= left + "AND" + right
        new_statement = "&".join(remove_dupes)
        xreplace= new_statement.replace("&()&","&")
        totalCNF = xreplace
    return totalCNF

def transformCNF(cnf):
    print("Converting to DNF...")
    print("length of cnf is :", len(cnf))
    # left, right = cnf.split("AND")
    # print("computing left... length: ", len(left))
    # print("left: ",left)
    # left_s = simplify_logic(left)
    # print("left simplified to :",(str(left_s)).replace(" ", ""))
    # print("--------------------------")
    # print("computing right... length: ", len(right))
    # print("right: ", right)
    # right_s = simplify_logic(right)
    # print("right simplified to :",(str(right_s)).replace(" ", ""))
    # print("--------------------------")
    # print(left_s, " AND ", right_s)
    # simplify = simplify_logic(left_s&right_s)
    simplify=simplify_logic(cnf)
    print("simplified to ", (str(simplify)).replace(" ", ""))
    print("===========================")
    return simplify

def getReducts(DNF):
    print("Calculating the reducts")
    stringDNF = str(DNF)
    dnfArray = (stringDNF.replace(" ", "")).split("&")
    singles=[]
    tuples=[]
    for element in dnfArray:
        if len(element)==1:
            singles.append(element)
        else:
            tuples.append(element)
    finalArray = []
    if tuples==[]:
        print("REDUCTS: ", singles)
        finalArray = singles
    else:
        # for single_e in singles:
        #     for tuple_e in tuples:
        #         single_array = ((tuple_e.replace("(","")).replace(")","")).split("|")
        #         final = list(map((lambda x: single_e + x), single_array))
        #         print("REDUCT:", final)
        #         finalArray.append(final)
        #         print("===================")
        for tuple_e in tuples:
            single_array = ((tuple_e.replace("(","")).replace(")","")).split("|")
            for single_e in singles:
                single_array = list(map((lambda x: single_e + x), single_array))
            print("REDUCT: ",single_array)
            print("======================")
            finalArray.append(single_array)
    return finalArray


with open(file_name) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    column_names = []
    decision_table = {}
    for row in csv_reader:
        if line_count == 0:
            for column_name in row:
                column_names.append(column_name)
            line_count += 1
        else:
            row_stats = LinkedList()
            counter = 0
            for attribute in row:
                new_node = Node(attribute)
                row_stats.add_last(new_node)
                counter += 1
            decision_table[line_count-1]=row_stats
            line_count += 1
    print("the column_names are: ")
    for i in range(0, len(column_names)):
        print(column_names[i], " : ", i)
    decisionAttributeSelected = int(input("Please enter the number of your decision attribute: "))
    reductMatrix = createMatrix(decision_table, decisionAttributeSelected)
    print("finished creating matrix")
    thisCNF = createCNF(reductMatrix)
    print("finished creating the CNF")
    thisDNF = transformCNF(thisCNF)
    print("finsihed converting to DNF")
    resRed = getReducts(thisDNF)
    print("the reducts are : ")
    print(resRed)
