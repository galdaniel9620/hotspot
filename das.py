
# for this task, i try to build a mesh using OOP

from element import Element
from node import Node
from value import Value

node_array = []  # matrix for nodes
element_array = []  # matrix for element
value_array = []  # matrix for values
hotspot_array = []
aux_array = element_array

# open file and store data in arrays
# i use "try" function because if there is no read file the code will not run and it will display a error message

# read the input file

with open("mesh_x_sin_cos_10000.txt", "r") as f :  # read the file
    lines = [line.strip() for line in f.readlines()]
    try :
        nodes_idx = lines.index("NODES")
        elements_idx = lines.index("ELEMENTS")
        values_idx = lines.index("VALUES")

        if not nodes_idx < elements_idx < values_idx :
            raise ValueError()

        nodes = [eval(line) for line in
                 lines[nodes_idx + 1 : elements_idx]]  # make the tuple list for nodes, elements and values
        elements = [eval(line) for line in lines[elements_idx + 1 : values_idx]]
        values = [eval(line) for line in lines[values_idx + 1 : :]]

        for i in nodes :  # for each tuple save the values into arrays
            aux = Node(i[0], i[1], i[2])
            node_array.append(aux)
        for j in elements :
            aux = Element(j[0], j[1], j[2], j[3])
            element_array.append(aux)
        for k in range(len(element_array)) :
            element_array[k].value = values[k][1]

    except ValueError :  # error message
        print("Invalid mesh file format")

# sort value array

element_array.sort(key=lambda x : x.value, reverse=True)


def isNeighbor(e1, e2) :  # find neighbors
    if e1.node1 == e2.node1 or e1.node1 == e2.node2 or e1.node1 == e2.node3 :  # the function isNeighbor check if an
        # element has neighbor, comparing the nodes from 2 elements and return true or false
        return True
    if e1.node2 == e2.node1 or e1.node2 == e2.node2 or e1.node2 == e2.node3 :
        return True
    if e1.node3 == e2.node1 or e1.node3 == e2.node2 or e1.node3 == e2.node3 :
        return True
    return False


for i in element_array : 
    for j in aux_array :
        if isNeighbor(i, j) and i.id != j.id :
            if j.id not in i.neighbors :
                i.neighbors.append(j.id)


# find hotspot

def markAsVisited(lst) :  # check is the element was visited and return true
    for ls in lst :
        for el in element_array :
            if el.id == ls :
                el.visited = True


def getElement(id) :
    for el in element_array :
        if el.id == id :
            return el


def findHotspot(N) :
    while N >= 1 :
        for x in element_array :
            is_hotspot = True  # start with the assumption that first element is a hotspot
            for y in x.neighbors :
                if x.value < getElement(y).value :
                    is_hotspot = False
                    break
                x.is_hotspot = is_hotspot
            if is_hotspot :  # if is hotspot, the function maskAsVisited is called to mark visited neighborhood
                x.visited = True
                markAsVisited(x.neighbors)
                print(x.value,x.id)
                N -= 1

# call the function findHotspot

findHotspot(int(input("N :")))

